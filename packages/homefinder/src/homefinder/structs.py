'''
Data structures for finding homes.

This module consists of data structures for real estate property
managment. These interfaces are more often then not automatically
constructed but they can be safely used by themselves.

Usage example:

```python
from homefinder.structs import *

price = Price(550.0, '€', Recurrence.Month)
print(price)  # Expected output: '550.0€/Month'

address = Address(
	country = 'Latvija',
	city    = 'Rīga',
	street  = 'Āzenes iela 12/1',
	code    = 'LV-1048'
)
print(address)  # Expected output: 'Āzenes iela 12/1, Rīga, Latvija, LV-1048'

home = Home(
	id      = 'DITEF',
	contact = 'tel:+37167089901',
	area    = 420.0,
	address,
	price
)
```
'''

from enum   import *
from typing import *


class Recurrence(Enum):
	'''Types of recurrence.'''

	No    = 0
	Day   = 1
	Month = 2
	Year  = 3

class Price(NamedTuple):
	'''Named tuple of a price tag.'''

	value: float
	'''Numerical value of the price.'''

	currency: str
	'''Monetary currency of the price.'''

	recurrance: Recurrence = Recurrence.No
	'''Type of lease recurrance.'''

	def __str__(self) -> str:
		if self.recurrance == Recurrence.No:
			return f'{ self.value }{ self.currency }'
		return f'{ self.value }{ self.currency }/{ self.recurrance.name }'		

class Address(NamedTuple):
	'''Named tuple of a geographical address.'''

	code: str
	'''Postal code of the address.'''

	county: str
	'''Country where the address is located.'''

	city: str
	'''City that holds the address.'''

	street: str
	'''Street name and number of the address.'''

	def __str__(self) -> str:
		return f'{ self.street }, { self.city }, { self.country }, { self.code }'

class Home(NamedTuple):
	'''
	Named tuple of a real estate property.

	This is the central interface used by `homefinder` compatible
	projects describing the data attributes a real estate property
	is expected to hold.
	'''

	id: str
	'''Unique identifier of the home.'''

	address: Address
	'''Home address.'''

	price: Price
	'''Monetary price of the home.'''

	area: float
	'''Square meter area of the home.'''

	contact: str
	'''URI for contacting the home seller.'''

	source: Optional['homefinder.Source'] = None
	'''Source of the home instance.'''

	images: list[str] = []
	'''List of image URIs associated with the home.'''

