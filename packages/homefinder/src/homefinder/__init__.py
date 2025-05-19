'''
Programmable interfaces for finding homes.

This package holds the core interfaces required for real estate managment
including a class for describing homes, `Home`, a protocol for finding them
online, `Source`, and other useful interfaces.

The included classes and modules are exclusively of the descriptive nature.
They contain little to no actual feature implementations, instead they
describe the way other projects shall interact with each other.

Descriptive data structures for real estate objects can be found in
`homefinder.structs` whereas functional interfaces like `Source` are
found in `homefinder.interfaces`.

Usage example:

```python
import homefinder

class MySource(homefinder.Source):
	name       = 'My Example Source'
	public_url = 'https://example.org'

	async def get_home(self, id):
		return homefinder.Home(id, ...)  # Construct a Home for id.

	async def search(self, params):
		for id in params.ids:
			yield self.get_home(id)  # Yield Homes.

source = MySource()
params = { 'ids': [ 0, 42 ] }  # Example params supplies the wanted ids.

async for home in source.search(params):
	print(home.price)
```
'''

from .structs import (
	Recurrence,
	Price,
	Address,
	Home
)

from .interfaces import (
	SearchParams,
	Source
)

