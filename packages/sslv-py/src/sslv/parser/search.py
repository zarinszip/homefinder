from typing import *

import asyncio
import re

from .base import HtmlStreamIter

type SearchYield = str | int
'''Value yielded by SearchIter.'''

type TagAttrs = List[Tuple[str, Optional[str]]]
'''List of HTML tag attribute tuple pairs.'''

class SearchIter(HtmlStreamIter[SearchYield]):
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

	queue: asyncio.Queue[Optional[SearchYield]] = asyncio.Queue()  # TODO: set maxsize?

	discover_pagecount: bool

	in_table: bool = False
	in_entry: bool = False

	after_table: bool = False
	end_of_info: bool = False


	def __init__(self, discover_pagecount: bool = False):
		HtmlStreamIter.__init__(self)
		self.discover_pagecount = discover_pagecount


	def __aiter__(self) -> AsyncIterator[str]:
		return self

	async def __anext__(self) -> SearchYield:
		if self.end_of_info:
			raise StopAsyncIteration

		ret = await self.queue.get()
		if ret == None:
			self.end_of_info = True
			while not self.queue.empty():
				self.queue.get_nowait()  # Empty the queue

			raise StopAsyncIteration

		return ret


	def feed(self, data: str):
		print(f'feed { data }')
		if self.end_of_info:
			return
		super().feed(data)

	def handle_starttag(self, tag: str, attrs: TagAttrs):
		print(f'handle_starttag { tag } { attrs }')
		match tag:
			case 'table':
				for (key, _) in attrs:
					if key == 'align':
						self.in_table = True
						return
			case 'tr':
				if not self.in_table:
					return

				for (key, val) in attrs:
					if key == 'id' and val != None:
						if val == 'head_line':
							return
						if val.startswith('tr_bnr_'):
							return
						break

				self.in_entry = True
			case 'a':
				if not self.in_entry and not (self.discover_pagecount and self.after_table):
					return

				if self.discover_pagecount and self.after_table:
					is_nav_id = False
					is_prev   = False

					for (key, val) in attrs:
						if key == 'name' and val == 'nav_id':
							is_navi = True
							continue
						if is_nav_id and key == 'rel' and val == 'prev':
							is_prev = True
							continue
						if is_prev and key == 'href' and val != None:
							result = re.search(r'/page([0-9]+).html$', val)
							if not result:
								continue

							pages = result.group(1)
							if not pages:
								continue

							self.queue.put_nowait(int(pages))
							self.queue.put_nowait(None)
							break
					return

				for (key, val) in attrs:
					if key == 'href' and val != None:
						result = re.search(r'/([a-z]+)\.html$', val)
						if not result:
							continue

						id = result.group(1)
						if not id:
							continue

						self.queue.put_nowait(id)
						self.in_entry = False
						break

	def handle_endtag(self, tag: str):
		print(f'handle_endtag { tag }')
		match tag:
			case 'table':
				if not self.in_table:
					return

				self.in_table    = False
				self.after_table = True

				if not self.discover_pagecount:
					self.queue.put_nowait(None)
			case 'tr':
				self.in_entry = False

