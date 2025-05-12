from typing import *

from .home import Home

type SearchParams = Optional[Mapping[str, Any]]
type SearchIter   = AsyncIterator[Home]

class Source(Protocol):
	'''
	Protocol for retrieving Home instances from online sources.

	Attributes:
		name: The display name of the source.
		public_url: An visitable URL to the source.
	'''

	name:       str
	public_url: str

	async def search(self, params: SearchParams) -> SearchIter:
		'''
		Find Homes.

		Args:
			params: Implementation specific dict that describes the
			        means as how to conduct a search. Not guaranteed
			        to always supply all required fields.

		Yields:
			Instances of Home as found by the online source.
		'''
		pass

	async def get_home(self, id: Any) -> Optional[Home]:
		'''Return an instance of Home for the given identifier.'''
		pass

