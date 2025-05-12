from typing import *

import homefinder_lib as lib

class Sludinajumi(lib.Source):
	'''
	`homefinder` source for SS.lv adverts.

	Example:
		import sslv

		ss   = sslv.Sludinajumi()
		args = {
			'city':      'Riga',
			'district':  'Agenskalns',
			'agreement': 'hand_over'
		}

		async for home in ss.search(args):
			print(home.address)
	'''

	name:       Final[str] = 'SS.lv Sludinājumi'
	public_url: Final[str] = 'https://www.ss.lv'

	async def search(self, params) -> lib.SearchIter:
		# TODO
		pass

	async def get_home(self, id: str) -> Optional[lib.Home]:
		# TODO
		pass

