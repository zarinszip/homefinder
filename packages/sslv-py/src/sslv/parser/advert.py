import homefinder as hf

from .base import HtmlStreamBuilder

class AdvertBuilder(HtmlStreamBuilder[hf.Home]):
	'''
	Parser for SS.lv advert entries.

	Supported content can be fetched via the following URLs:
	- https://www.ss.lv/msg/{lang}/real-estate/{type}/{city}/{destrict}/{agreement}/{id}.html
	- https://www.ss.lv/msg/{id}.html (expanded by SS.lv itself)
	'''
	# TODO
	pass

