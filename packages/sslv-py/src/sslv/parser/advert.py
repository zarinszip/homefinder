from html import parser

class AdvertParser(parser.HTMLParser):
	'''
	Parser for SS.lv advert entries.

	Supported content can be fetched via the following URLs:
	- https://www.ss.lv/msg/{lang}/real-estate/{type}/{city}/{destrict}/{agreement}/{id}.html
	- https://www.ss.lv/msg/{id}.html (expanded by SS.lv itself)

	As input it takes an aiohttp.StreamReader, turning it into a
	valid homefinder_lib.Home.
	'''
	# TODO
	pass

