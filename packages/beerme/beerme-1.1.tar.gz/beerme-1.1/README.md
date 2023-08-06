# BeerMe

beerme is an untapped scraper for Big Hops locations in San Antonio, TX.
I built this utility because javascript page flipper is either too slow or too fast
(depending on which page you are looking at). Untapped does provide API access, but
only to certain individuals.

## Installation
```shell
$ pip install beerme
```

If that does not work, make sure you have python and pip installed. Also, you may need to use
sudo or the `--user` flag for `pip`

## Usage

```
usage: beerme [-h] [--list] [-J] [--dump] [-p] [-d] [-f] [-s SEARCH]
              [-e EXCLUDE]
              [location]

BeerMe BigHops script 0.9

positional arguments:
  location              Beer target

optional arguments:
  -h, --help            show this help message and exit
  --list                list available locations
  -J, --json            Output information in json
  --dump                Dump the raw tap list html
  -p, --show-prices     Show price and volume data
  -d, --draft-only      Exclude bottles and cans
  -f, --fills-only      Only include beer that can be purchased in growlers
  -s SEARCH, --search SEARCH
                        A keyword to search for. For example: "IPA". This can
                        be used multiple times to create a compound search
  -e EXCLUDE, --exclude EXCLUDE
                        A keyword used to exclude results. For example:
                        "Sour". This can be used multiple times
```
For example:

```
$ beerme bh-bitters -s IPA -s Pale -e Imperial
Tejas Clara / Big Bend
Lager - Pale | 4.3% ABV

Merry Buffing Xmas / Buffalo Bayou
IPA - American brewed with Spruce tips | 7.6% ABV

Axis IPA / Real Ale
IPA - American | 7% ABV

Pub Crawl / Saint Arnold
Pale Ale - American | 4.7% ABV

Syncopation / NOLA
IPA - American | 6% ABV

Celebration Ale / Sierra Nevada
IPA - American | 6.8% ABV

Accumulation (2018) / New Belgium
IPA - White | 6.2% ABV

Citradelic: Tangerine IPA / New Belgium
IPA - American | 6% ABV

SMaSh and GRaB / Legal Draft Beer
IPA - American | 6.2% ABV
```

## Locations

Currently, I have hard code the following location map in the source

```python
location_map = {
    'bh-bridge': 'https://business.untappd.com/boards/24264',
    'bh-bitters': 'https://business.untappd.com/boards/24239',
    'bh-huebner': 'https://business.untappd.com/boards/24278',
    'bh-shaenfield': 'https://business.untappd.com/boards/27711'
}
```

It should be trivial to adapt this source to work with other locales

## Notice

I do not represent Big Hops or Untapped in any way. Use this software at your own risk.

