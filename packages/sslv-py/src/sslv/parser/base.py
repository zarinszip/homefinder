from typing import *

from html import parser

class HtmlStreamBuilder[T](parser.HTMLParser):
	'''A HTMLParser that may return something as it's fed.'''

	def __init__(self):
		parser.HTMLParser.__init__(self)

	def feed(self, data: str) -> Optional[T]:
		parser.HTMLParser.feed(self, data)
		return None

class HtmlStreamIter[T](parser.HTMLParser, AsyncIterable[T]):
	'''
	An iterable version of HTMLParser.

	Should probably internally use asyncio.Queue.
	'''

	def __init__(self):
		parser.HTMLParser.__init__(self)

