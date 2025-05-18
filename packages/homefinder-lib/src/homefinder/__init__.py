'''
Functional interfaces for finding homes.

This includes a class for homes, a protocol for finding them
online, and so on.
'''

from .structs import (
	Recurrence,
	Price,
	Address,
	Home
)

from .source import (
	Source,
	SearchParams,
	SearchIter
)

