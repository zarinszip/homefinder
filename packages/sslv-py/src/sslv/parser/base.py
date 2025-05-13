from typing import *

from html import parser

class HtmlStreamBuilder[T](parser.HTMLParser):
	'''A HTMLParser that may return something as it's fed.'''

	def feed(self, data: str) -> Optional[T]:
		parser.HtmlParser.feed(self, data)
		return None

class HtmlStreamIter[T](parser.HTMLParser, AsyncIterable[T]):
	'''
	An iterable version of HTMLParser.

	Should probably internally use asyncio.Queue.
	'''
	pass

