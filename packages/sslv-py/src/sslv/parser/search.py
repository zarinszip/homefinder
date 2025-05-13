from .base import HtmlStreamIter

class SearchIter(HtmlStreamIter[str]):
	'''
	Iterator for SS.lv search results.

	Supported content can be fetched via the following URLs:
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/filter/ (POST HTML form)
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/filter/page{page}.html (paging)
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/
	- https://www.ss.lv/lv/real-estate/{type}/{city}/{district}/page{page}.html (paging)
	'''
	# TODO
	pass

