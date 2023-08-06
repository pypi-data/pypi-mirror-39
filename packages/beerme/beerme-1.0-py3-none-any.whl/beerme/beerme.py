#!/usr/bin/env python

import sys

import argparse
import json
import requests

from bs4 import BeautifulSoup

from . import get_version


location_map = {
    'bh-bridge': 'https://business.untappd.com/boards/24264',
    'bh-bitters': 'https://business.untappd.com/boards/24239',
    'bh-huebner': 'https://business.untappd.com/boards/24278',
    'bh-shaenfield': 'https://business.untappd.com/boards/27711'
}

span_items = [
    'brewery',
    'name',
    'style',
    'abv',
    'ibu',
    'brewery-location'
]


def get_tap_list(script_data):
    tap_list = []
    for line in [_l.strip() for _l in script_data.splitlines()]:
        if not line:
            continue
        var, value = line.split('=', 1)
        if var.strip() == 'window.ITEMS_ARRAY':
            scrubbed = value.strip(';')
            tap_list = json.loads(scrubbed)
            break
    return tap_list


def parse_containers(containers):
    _containers = []
    container_items = containers.find_all('span', {'class': 'container-item'})
    for container_item in container_items:
        container_dict = {}
        for container_element in container_item.children:
            _class = container_element.attrs['class'][0]
            if _class == 'price':
                container_dict['price'] = container_element.contents[1]
            else:
                container_dict[_class.replace('-', '_')] = container_element.string.strip()
        _containers.append(container_dict)
    return _containers


def parse_info(tap_list):
    parsed_tap_list = []
    for page in tap_list:
        soup = BeautifulSoup(page['html'], 'html.parser')
        info_elements = soup.find_all('div', {'class': 'info'})
        for info_element in info_elements:
            info_dict = {}
            for item in span_items:
                result = info_element.find('span', {'class': item})
                if result:
                    info_dict[item.replace('-', '_')] = result.string.strip()
                else:
                    info_dict[item.replace('-', '_')] = None
            containers = info_element.find('div', {'class': 'containers'})
            info_dict['containers'] = parse_containers(containers)
            parsed_tap_list.append(info_dict)
    return parsed_tap_list


def list_locations():
    for location, taplist in location_map.items():
        print('{} : {}'.format(location, taplist))


def list_output(data, show_containers=False):
    for bev in data:
        print('{name} / {brewery}\n{style} | {abv}'.format(**bev))
        if show_containers:
            for container in bev['containers']:
                print('\t{} ${} {}'.format(
                    container.get('name'),
                    container.get('price'),
                    container.get('container_calories')))
        print()

def bottle_or_can_filter(bev):
    for container in bev['containers']:
        if 'Bottle' in container['name'] or 'Can' in container['name']:
            return False
    return True

def keyword_search(bev, search_terms):
    for key in bev:
        if key == 'containers':
            continue
        for search_term in search_terms:
            if bev[key]:
                if search_term.lower() in bev[key].lower():
                    return True
    return False

def keyword_filter(bev, search_terms):
    for key in bev:
        if key == 'containers':
            continue
        for search_term in search_terms:
            if bev[key]:
                if search_term.lower() in bev[key].lower():
                    return False
    return True

def main():
    a = argparse.ArgumentParser(
        'beerme',
        description='BeerMe BigHops script {}'.format(get_version()))
    a.add_argument('--list', action='store_true', help='list available locations')
    a.add_argument('-J', '--json', action='store_true', help='Output information in json')
    a.add_argument('--dump', action='store_true', help='Dump the raw tap list html')
    a.add_argument('location', help='Beer target', default='', nargs='?')
    a.add_argument('-p', '--show-prices', action='store_true', help='Show price and volume data')
    a.add_argument('-d', '--draft-only', action='store_true', help='Exclude bottles and cans')
    a.add_argument('-f', '--fills-only', action='store_true',
        help='Only include beer that can be purchased in growlers')
    a.add_argument('-s', '--search', action='append', help='A keyword to search for. For example: "IPA". '
                   'This can be used multiple times to create a compound search')
    a.add_argument('-e', '--exclude', action='append', help='A keyword used to exclude results. For example: "Sour". '
                   'This can be used multiple times')
    namespace = a.parse_args()

    if namespace.list:
        list_locations()
        sys.exit(0)

    if not namespace.location:
        print('Location not provided')
        a.print_usage()
        sys.exit(1)

    url = location_map.get(namespace.location)
    if not url:
        print('{} does not exist'.format(namespace.location))
        list_locations()
        sys.exit(1)

    _data = requests.get(url).text

    tap_list_page = BeautifulSoup(_data, 'html.parser')
    # Currently, the first script is the one we want
    _tap_list = get_tap_list(tap_list_page.find('script').string)

    if namespace.dump:
        for i, page in enumerate(_tap_list):
            with open('{}-taplist-{}.html'.format(namespace.location, i), 'w') as fp:
                fp.write(page['html'])
        sys.exit(0)

    tap_data = parse_info(_tap_list)

    if namespace.draft_only:
        tap_data = filter(bottle_or_can_filter, tap_data)

    if namespace.search:
        tap_data = filter(lambda bev: keyword_search(bev, namespace.search), tap_data)
    if namespace.exclude:
        tap_data = filter(lambda bev: keyword_filter(bev, namespace.exclude), tap_data)
    if namespace.json:
        print(json.dumps(tap_data, indent=2))
    else:
        list_output(tap_data, namespace.show_prices)


if __name__ == '__main__':
    main()
