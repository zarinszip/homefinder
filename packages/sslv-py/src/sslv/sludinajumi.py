from typing import *

from . import parser

import homefinder as home
import aiohttp

from encodings import utf_8


type MinMax[T] = tuple[T, T]

class SludinajumiSearchParams(TypedDict):
	housing_type: str
	location:     str

	catastral_num: str

	deal_type: str
	deal_age:  str
	sort:      str

	query: str

	rooms: MinMax[str]
	area:  MinMax[str]
	floor: MinMax[str]
	price: MinMax[str]

	historical_period: list[str]

	material:   list[str]
	facilities: list[str]

	lift: bool

type SludinajumiSearchForm = TypedDict('SludinajumiSearchForm', {
	'topt[1631]': str,  # Catastral number

	'sid':  Literal['', '1', '6', '3'],  # Deal type: All, Sell, Hand over, Change
	'pr':   str,                         # Period (in days back, all: 0)
	'sort': str,                         # Sort

	'txt': str,  # Text query

	'topt[1][min]': str,  # Rooms
	'topt[1][max]': str,
	'topt[3][min]': str,  # Area
	'topt[3][max]':	str,
	'topt[4][min]': str,  # Floor
	'topt[4][max]': str,
	'topt[8][min]': str,  # Price
	'topt[8][max]':	str,

	'opt[6][]': str,  # Historical period

	'opt[2][]':    str,  # House material
	'opt[1734][]': str,  # Facilities

	'opt[367]': Literal['', '8041'],  # Lift

	'btn': Literal['Search']  # Initiator
})



class Sludinajumi(home.Source):
	'''
	`homefinder` source for SS.lv adverts.

	Example:
		import sslv

		ss   = sslv.Sludinajumi()
		args = {
			'housing_type': 'flats',
			'location':     'riga/agenskalns',
		}

		async for home in ss.search(args):
			print(home.address)
	'''

	name:       Final[str] = 'SS.LV Sludinājumi'
	public_url: Final[str] = 'https://www.ss.lv'

	session: aiohttp.ClientSession


	def __init__(self):
		self.session = aiohttp.ClientSession()

	@staticmethod
	def map_params(params: SludinajumiSearchParams) -> SludinajumiSearchForm:
		return {
			'topt[1631]': params.get('catastral_num', ''),

		        'sid':  params.get('deal_type', ''),
		        'pr':   params.get('deal_age', '0'),
        		'sort': params.get('sort', '0'),

		        'txt': params.get('query', ''),

		        'topt[1][min]': params.get('rooms', ('0', '0'))[0],
		        'topt[1][max]': params.get('rooms', ('0', '0'))[1],
		        'topt[3][min]': params.get('area',  ('', ''))[0],
		        'topt[3][max]': params.get('area',  ('', ''))[1],
		        'topt[4][min]': params.get('floor', ('', ''))[0],
		        'topt[4][max]': params.get('floor', ('', ''))[1],
		        'topt[8][min]': params.get('price', ('', ''))[0],
		        'topt[8][max]': params.get('price', ('', ''))[1],

			'opt[6][]': ','.join(params.get('historical_period', [])),

			'opt[2][]':    ','.join(params.get('material', [])),
			'opt[1734][]': ','.join(params.get('facilieties', [])),

			'opt[367]': '8041' if params.get('lift', False) else '',

			'btn': 'Search'
		}


	async def resolve(self, id: str) -> Optional[home.Home]:
		async with self.session.get(f'{ self.public_url }/msg/{ id }.html') as response:
			if response.status != 200:
				return None

			builder = parser.AdvertBuilder()
			decoder = utf_8.IncrementalDecoder(errors = 'replace')
			result  = None

			async for chunk in response.content.iter_any():
				result = builder.feed(decoder.decode(chunk), id)
				if result != None:
					break

			return result

	async def search(self, params: SludinajumiSearchParams) -> AsyncIterator[home.Home]:
		url = f'{ self.public_url }/en/real-estate/{ params['housing_type'] }/{ params['location'] }/search-result/'

		init = await self.session.post(url, data = self.map_params(params))
		init.release()
		if init.status != 200:
			return

		init = await self.session.get(f'{ self.public_url }/w_inc/chk.php?mm=1&c=1088&db=en&mode=1&g=1')
		init.release()
		if init.status != 200:
			return

		page  = 1
		count = 1
		while not page > count:
			async with self.session.get(f'{ url }page{ page }.html') as response:
				if response.status != 200:
					return

				first = page == 1
				iter  = parser.SearchIter(
					inner = response.content.iter_any(),
					discover_pagecount = first
				)

				async for id in iter:
					print(id)
					home = await self.resolve(id)
					if home is not None:
						yield home

				page += 1
				if first and iter.pagecount is not None:
					count = iter.pagecount

