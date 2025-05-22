import sys
import asyncio
import sslv
from openpyxl import Workbook
from typing import List, Union
import homefinder as hf

def parse_minmax(value: str) -> tuple[str, str]:
    parts = value.split(':')
    if len(parts) != 2:
        return ('', '')  # default empty tuple
    return parts[0], parts[1]

def parse_list(value: str) -> list[str]:
    if not value:
        return []
    return value.split(',')

def parse_bool(value: str) -> bool:
    return value.lower() in ['true', '1', 'yes']

async def main():
    raw_args = sys.argv[1:]
    search_params = {}
    end_of_args = False
    i = 0

    while i < len(raw_args):
        arg = raw_args[i]
        if '=' in arg:
            key, val = arg.split('=', 1)
            match key:
                case 'rooms' | 'area' | 'floor' | 'price':
                    search_params[key] = parse_minmax(val)
                case 'historical_period' | 'material' | 'facilities':
                    search_params[key] = parse_list(val)
                case 'lift':
                    search_params[key] = parse_bool(val)
                case 'location':
                     search_params[key] = val.replace('_', '-').replace('.', '')
                case _:
                     search_params[key] = val
            i += 1

    async with sslv.Sludinajumi() as ss:
        homes = []
        async for home in ss.search(search_params):
            print('------------------------------------')
            print(home)
            homes.append(home)
        homes_to_excel(homes)

def homes_to_excel(homes: Union[hf.Home, List[hf.Home]], filename: str = "homes.xlsx"):
    if not isinstance(homes, list):
        homes = [homes]

    wb = Workbook()
    ws = wb.active
    ws.title = "Homes"

    headers = ["ID", "Address", "Price", "Area", "Contact", "Source", "Images"]
    ws.append(headers)

    for home in homes:
        row = [
            home.id,
            str(home.address),
            str(home.price),
            home.area,
            home.contact,
            str(home.source) if home.source else "",
            ", ".join(home.images) if home.images else ""
        ]
        ws.append(row)

    wb.save(filename)

def exec():
	asyncio.run(main())

if __name__ == "__main__":
    exec()
