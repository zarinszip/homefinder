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

	id: str
	city: str				# e.g. "Riga"
	district: str				# e.g. "Centre"
	street: str				# e.g. "Klusa 7"
	area: str	 			# in m²
	price: str				# in €
	facilities: Optional[str]		# e.g. "Balcony, Parking"

	def __str__(self):
		return f'id: {self.id}\ncity: {self.city}\ndistrict: {self.district}\nstreet: {self.street}\narea: {self.area}\nprice: {self.price}\nfacilities: {self.facilities}'

