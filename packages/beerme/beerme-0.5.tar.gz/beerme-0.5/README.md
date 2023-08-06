# BeerMe

beerme is an untapped scraper for Big Hops locations in San Antonio, TX.
I built this utility because javascript page flipper is either too slow or too fast
(depending on which page you are looking at). Untapped does provide API access, but
only to certain individuals.

## Usage

This version of beerme only has `json` output support. I will add console formatted output
and the ability to filter, sort, and search at some point in the future. 

```
usage: beerme [-h] [--list] [-J] [--dump] [location]

BeerMe BigHops script v0.4

positional arguments:
  location    Beer target

optional arguments:
  -h, --help  show this help message and exit
  --list      list available locations
  -J, --json  Output information in json
  --dump      Dump the raw tap list html
```

## Notice

I do not represent Big Hops or Untapped in anyway. Use this software at your own risk.

