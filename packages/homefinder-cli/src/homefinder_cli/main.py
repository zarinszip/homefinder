import sys
import asyncio
import sslv

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

def build_search_params(partial: dict) -> sslv.sludinajumi.SludinajumiSearchParams:
    # Fill all required keys with defaults if missing
    return sslv.sludinajumi.SludinajumiSearchParams(
        housing_type = partial.get('housing_type', ''),
        location = partial.get('location', ''),
        catastral_num = partial.get('catastral_num', ''),
        deal_type = partial.get('deal_type', ''),
        deal_age = partial.get('deal_age', ''),
        sort = partial.get('sort', ''),
        query = partial.get('query', ''),
        rooms = partial.get('rooms', ('', '')),
        area = partial.get('area', ('', '')),
        floor = partial.get('floor', ('', '')),
        price = partial.get('price', ('', '')),
        historical_period = partial.get('historical_period', []),
        material = partial.get('material', []),
        facilities = partial.get('facilities', []),
        lift = partial.get('lift', False),
    )

async def main():
    raw_args = sys.argv[1:]
    parsed_args = {}
    end_of_args = False
    i = 0

    while i < len(raw_args):
        arg = raw_args[i]
        if not end_of_args:
            match arg:
                case '--filter' | '-f':
                    i += 1
                    while i < len(raw_args) and '=' in raw_args[i]:
                        key, val = raw_args[i].split('=', 1)
                        match key:
                            case 'rooms' | 'area' | 'floor' | 'price':
                                parsed_args[key] = parse_minmax(val)
                            case 'historical_period' | 'material' | 'facilities':
                                parsed_args[key] = parse_list(val)
                            case 'lift':
                                parsed_args[key] = parse_bool(val)
                            case _:
                                parsed_args[key] = val
                        i += 1
                    continue
                case '--module':
                    i += 2
                case '--':
                    end_of_args = True
                case _:
                    i += 1
        else:
            if '=' in arg:
                key, val = arg.split('=', 1)
                match key:
                    case 'rooms' | 'area' | 'floor' | 'price':
                        parsed_args[key] = parse_minmax(val)
                    case 'historical_period' | 'material' | 'facilities':
                        parsed_args[key] = parse_list(val)
                    case 'lift':
                        parsed_args[key] = parse_bool(val)
                    case 'location':
                        parsed_args[key] = val.replace('_', '-').replace('.', '')
                    case _:
                        parsed_args[key] = val
            i += 1

    search_params = build_search_params(parsed_args)

    print("Final search params:", search_params)

    ss = sslv.Sludinajumi()
    async for home in ss.search(search_params):
        print('------------------------------------')
        print(home)

if __name__ == "__main__":
    asyncio.run(main())
