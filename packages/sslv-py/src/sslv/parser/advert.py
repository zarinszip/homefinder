import homefinder as hf
from typing import Optional
from .base import HtmlStreamBuilder
from dataclasses import fields
import re

class AdvertBuilder(HtmlStreamBuilder[hf.Home]):
    def __init__(self):
        super().__init__()
        self._id_map = {
            'tdo_20': 'city',
            'tdo_856': 'district',
            'tdo_11': 'street',
            'tdo_3': 'area',
            'tdo_8': 'price',
            'tdo_1734': 'facilities',
        }
        self._attrs = set(self._id_map.keys())
        self._home = hf.Home(id=None, city=None, district=None, street=None, area=None, price=None, facilities=None)
        self._current_field = None
        self._buffer = []
        self._inside_target_td = False
        self._inside_link = False
        self._inside_ignored_span = False

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            attrs_dict = dict(attrs)
            td_id = attrs_dict.get("id")

            if td_id in self._attrs:
                self._current_field = self._id_map[td_id]
                self._buffer = []
                self._inside_target_td = True

        elif tag == "a" and self._inside_target_td:
            self._inside_link = True

        elif tag == "span" and self._inside_target_td:
            attrs_dict = dict(attrs)

            if attrs_dict.get("class") == "td15":
                self._inside_ignored_span = True

    def handle_endtag(self, tag):
        if tag == "td" and self._inside_target_td:
            value = ' '.join(self._buffer).strip()

            if self._current_field:
                setattr(self._home, self._current_field, value)
            self._inside_target_td = False
            self._current_field = None
            self._buffer = []

        elif tag == "a":
            self._inside_link = False

        elif tag == "span":
            self._inside_ignored_span = False

    def handle_data(self, data):
        if self._inside_target_td and not self._inside_link and not self._inside_ignored_span:
            text = data.strip()
            if text:
                self._buffer.append(text)

    def extract_id(self, url: str) -> Optional[str]:
        match = re.search(r'/([a-z0-9]+)\.html$', url)
        if match:
            return match.group(1)
        return None

    def feed(self, data: str, url: str) -> Optional[hf.Home]:
        super().feed(data)
        home_field_names = [f.name for f in fields(hf.Home)]
        field_vals = {name: getattr(self._home, name, None) for name in home_field_names}
        if 'id' in home_field_names and url:
            field_vals['id'] = self.extract_id(url)

        return hf.Home(**field_vals)
