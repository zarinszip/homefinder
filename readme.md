# `homefinder`

> Martins Zariņš (241RDB186)

> Rauls Ulvis Grimza (241RDB178)


## Projekta uzdevums

`homefinder` ir vairāku mazāku projektu kolekcija, kas, kopā strādājot,
atļauj automatizēt nekustamā īpašuma meklēšanu, analizēšanu un filtrēšanu.

Pythona pakete vārdā `homefinder` definē tipētas datu struktūras, kas definē
kādas īpašības piemīt nekustamam īpašumam, kā tie sadarbojās savstarpā un kā
tos var atrast no tīkla avotiem. Šīs datu struktūrās ir lielākoties `Protocol`
un `NamedTuple` tipa, kas ir Python standarta bibliotēkas `typing` sastāvā.

`sslv-py` ir praktiska `homefinder.Source` implementācija, iegūstot `homefinder.Home`
instances no SS.LV mājaslapas satura.

`homefinder-cli` ir komandrindas rīks, kas ļauj lietotājam izmantot pārējās
projekta bibliotēkas standartizētā veidā. Tas iegūst argumentus no
komandrindas, dod tos `homefinder.Source` instancei (šeit `sslv.Sludinajumi`)
un saglabā iegūtos nekustamos īpašumus Excel failā.


## Programmas izmantošana

Pirms lietosanas manuāli jāinstalē projekta paketes. Tas automātiski
lejupielādēs nepieciešamās [PYPI bibliotēkas](#pypi-bibliotēkas), kā
arī pataisīs `homefinder` komandu pieejamu.

```sh
pip install -e packages/*
```

Pēc veiksmīgas ienstalēšanas `homefinder` lietojums izskatās sekojoši:

```sh
homefinder \
	housing_type=<flats|homes-summer-residences|offices|...> \
	location=<riga/agenskalns|jurmala|...> \
	[price=min:max] \
	[area=min:max] \
	[rooms=min:max] \
	[floor=min:max] \
	[filtri...]
```

Izpildot komandu, tiks ģenerēts `homes.xlsx` fails, kas satur visus
atrastos sludinājumus.

Iekšrindas dokumentāciju var apskatīt, lietojot `pdoc` rīku. Pēc tās
ielādes dokumentāciju var atvert interneta pārlūkā, ievadod sekojošo
komandu:

```sh
pdoc <module>
```


## Izmantotās bibliotēkas un rīki

### Komandrindas rīki

- `pdoc` HTML dokumentācijas ģenerators.
  Atļauj dokumentāciju klasēm rakstīt iekš koda definīcijā.
- `uv` Pythona projekta (`pyproject.toml`) pārvaldnieks.
  Atļauj modernā, standartizētā veidā definēt atkarības uz
  citām bibliotēkām, kā arī sadalīt projektu vairākās paketēs.

### Python standarta bibliotēka

- `asyncio` `async`/`await`implementācija.
- `encodings.utf_8` UTF-8 dekoders.
- `html.parser` HTML lasītājs.
- `re` regulārās izteiksmes.
- `typing` koda tipu definīcijas.
- `queue` datu klase.

### PYPI bibliotēkas

- `aiohttp` asinhrona HTTP klienta implementācija.
- `flit_core` Pythona projekta būvnieks.
  Izmantots sadarbībā ar `uv`.
- `openpyxl` Excel faila rakstītājs.


