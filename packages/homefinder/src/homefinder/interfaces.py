'''
Functional interfaces for finding homes.

This module centres primarily around the `Source` protocol, a interface
defining how to retrieve `Home` instances from the web.
'''

from typing import *

from homefinder import Home


type SearchParams = dict[str, Any]
'''Dictionary type for specifying search options.'''

class Source(Protocol):
	'''
	Protocol for retrieving `Home` instances from online sources.

	This is the primary protocol used in `homefinder` compatible projects
	to integrate with real estate websites.

	As this is only a protocol this class can not be constructed.
	'''

	name: str
	'''Display name of the source.'''

	public_url: str
	'''Visitable URL to the source.'''

	async def get_home(self, id: Any) -> Optional[Home]:
		'''Return a `Home` for the given identifier if found.'''
		raise NotImplementedError

	async def search(self, params: Optional[SearchParams]) -> AsyncIterator[Home]:
		'''
		Find `Home` instances.

		Args:
			params: Implementation specific dict that describes the
		        	means as how to conduct a search.

		Yields:
			`Home` instances as provided by the online source.
		'''
		raise NotImplementedError

