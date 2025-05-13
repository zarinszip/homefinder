from dataclasses import *
from typing      import *

@dataclass
class Home:
	'''
	Dataclass of a house.

	TODO: Add attributes.

	Attributes:
		id: A unique, idempotent home identifier.
		city: ...
		district: ...
		street: ...
		area: Area for the real estate measured in m².
		price: Flat or monthly price for the real estate. Can include price per square metre.
		facilities: Additional facilities that may come with the real estate.
	'''

	id: Optional[str]
	city: Optional[str]				# e.g. "Riga"
	district: Optional[str]			# e.g. "Centre"
	street: Optional[str]			# e.g. "Klusa 7"
	area: Optional[str] 			# in m²
	price: Optional[str]			# in €
	facilities: Optional[str]		# e.g. "Balcony, Parking"

