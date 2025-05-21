import homefinder as hf
import re
from .base import HtmlStreamBuilder

class AdvertBuilder(HtmlStreamBuilder[hf.Home]):
	'''
	Parser for SS.lv advert entries.

	Supported content can be fetched via the following URLs:
	- https://www.ss.lv/msg/{lang}/real-estate/{type}/{city}/{destrict}/{agreement}/{id}.html
	- https://www.ss.lv/msg/{id}.html (expanded by SS.lv itself)
	'''
	def __init__(self):
		super().__init__()

		self._buffer = []
		self._id_list = ['tdo_3', 'tdo_8', 'tdo_11', 'tdo_20'] # area, price, street, city respectively
		self._curr_id = None

		self._id = None
		self._city = None
		self._street = None
		self._value = None
		self._currency = None
		self._recurrence = hf.Recurrence.No
		self._area = None
		self._contact = None
		self._images = []

	def handle_starttag(self, tag, attrs):
		attrs_dict = dict(attrs)

		match tag:

			case 'td':
				self._buffer.append('td')
				td_id = attrs_dict.get('id')
				if td_id in self._id_list:
					self._curr_id = td_id

			case 'b':
				if self._buffer and self._buffer[-1] == 'td':
					self._buffer.append('b')

			case 'div':
				if attrs and attrs[0][1] == 'pic_dv_thumbnail':
					self._buffer.append('div')

			case 'a':
				href = attrs_dict.get('href')
				if href and href.startswith('http') and href.endswith('.jpg'):
					self._images.append(href)


	def handle_endtag(self, tag):
		...

	def handle_data(self, data):
		if not self._buffer or not data.strip():
			return

		content = data.strip()

		match self._buffer[-1]:
			case 'b' | 'td':
				match self._curr_id:

					case 'tdo_20':

						self._city = content

					case 'tdo_11':

						self._street = content

					case 'tdo_8':

						matches = re.search(r'([\d\s]+)\s?(.)/([a-z]+)\.', content)

						self._value = matches.group(1)
						self._currency = matches.group(2)
						if not matches.group(3):
							self._recurrence = hf.Recurrence.No
						else:
							match matches.group(3):
								case 'mon':
									self._recurrence = hf.Recurrence.Month

								# add more if necessary

					case 'tdo_3':

						matches = re.search(r'([0-9]+)', content)
						if matches:
							self._area = matches.group(1)

				self._curr_id = None
				self._buffer.pop()

			case 'div':
				self._buffer.pop()


	def extract_id(self, url) -> str:
		'''
		Returns extracted id from the url, using regular expressions
		'''
		match = re.search(r'/([a-z]+)\.html$', url)
		if match:
			return match.group(1)
		return None

	def feed(self, data, id) -> hf.Home:
		super().feed(data)
		self._id = id

		return hf.Home (
			id = self._id,
			address = hf.Address(
				code = '',
				country = 'Latvija',
				city = self._city,
				street = self._street
			),
			price = hf.Price(
				value = float(self._value),
				currency = self._currency,
				recurrence = self._recurrence
			),
			area = self._area,
			contact = self._contact,
			images = self._images
		)

	pass

