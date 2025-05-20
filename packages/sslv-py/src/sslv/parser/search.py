from typing import *

from .base import HtmlStreamIter

from queue import Queue
import re

from encodings import utf_8


type TagAttrs = List[Tuple[str, Optional[str]]]
'''List of HTML tag attribute tuple pairs.'''

class SearchIter(HtmlStreamIter[str]):
	'''
	Iterator for SS.lv search results.

	Supported content can be fetched via the following URLs:
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/filter/ (POST HTML form)
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/filter/page{page}.html (paging)
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/page{page}.html (paging)

	Attributes:
		queue: Internal queue for storing ids/pagecounts as they are fed.
		discover_pagecount: Whether the iterator should find the maximum pagecount.
		in_table: State indicator for being in the correct table.
		in_entry: State indicator for being in a valid table entry.
		after_table: State indicator for having read the pages whole table.
		end_of_info: State indicator for having read all information of a page.
	'''

	inner:   AsyncIterator[bytes]
	decoder: utf_8.IncrementalDecoder

	queue:     Queue[str] = Queue()
	pagecount: Optional[int]

	in_title: bool = False
	in_table: bool = False
	in_entry: bool = False

	after_table:    bool = False
	in_page_button: bool = False

	end_of_data: bool = False


	def __init__(
		self, inner: AsyncIterator[bytes], *,
		utf8_errors:        str  = 'replace',
		discover_pagecount: bool = False
	):
		HtmlStreamIter.__init__(self)

		self.inner   = inner
		self.decoder = utf_8.IncrementalDecoder(errors = utf8_errors)

		self.pagecount = None if discover_pagecount else -1


	def __aiter__(self) -> AsyncIterator[str]:
		return self

	async def __anext__(self) -> str:
		if not self.queue.empty():
			return self.queue.get()

		if self.end_of_data:
			raise StopAsyncIteration

		try:
			chunk = await self.inner.__anext__()
		except StopAsyncIteration:
			self.end_of_data = True
			return await self.__anext__()

		self.feed(self.decoder.decode(chunk))
		return await self.__anext__()


	def handle_starttag(self, tag: str, attrs: TagAttrs):
		match tag:
			case 'title':
				self.in_title = True
			case 'table':
				for (key, _) in attrs:
					if key == 'align':
						self.in_table = True
						break
			case 'tr':
				if not self.in_table:
					return

				for (key, val) in attrs:
					if key == 'id' and val is not None:
						if val == 'head_line':
							return
						if val.startswith('tr_bnr_'):
							return
						break

				self.in_entry = True
			case 'a':
				if not (self.in_entry or (self.after_table and self.pagecount is None)):
					return

				if self.after_table and self.pagecount is None:
					is_nav_id = False
					is_prev   = False

					for (key, val) in attrs:
						if key == 'name' and val == 'nav_id':
							is_nav_id = True
							continue
						if is_nav_id and key == 'rel' and val == 'prev':
							is_prev = True
							continue
						if is_prev and key == 'href' and val is not None:
							result = re.search(r'/page([0-9]+).html$', val)
							if result is None:
								continue

							self.pagecount = int(result.group(1))
							break
					return

				for (key, val) in attrs:
					if key == 'href' and val is not None:
						result = re.search(r'/([a-z]+)\.html$', val)
						if result is None:
							continue

						self.queue.put(result.group(1))
						self.in_entry = False
						break
			case 'button':
				if not (self.after_table and self.pagecount is None):
					return

				for (key, val) in attrs:
					if key == 'class' and val == 'navia':
						self.in_page_button = True
						break

	def handle_endtag(self, tag: str):
		match tag:
			case 'table':
				if not self.in_table:
					return

				self.in_table    = False
				self.after_table = True

				if self.pagecount is not None:
					self.end_of_data = True
			case 'tr':
				self.in_entry = False

	def handle_data(self, data: str):
		if self.in_title:
			self.in_title = False
			if re.match(r'SS\.(LV|COM).*Search results', data):
				return

			self.end_of_data = True
			raise ValueError('HTML data is not a SS.LV search result page.')

		if self.in_page_button:
			self.in_page_button = False
			self.end_of_data    = True

			current_page = int(data)
			if (current_page == 1):
				return

			self.pagecount = None
			raise ValueError("SearchIter was constructed with 'dicover_pagecount = True', but HTML data is not page 1 of SS.LV search results.")

