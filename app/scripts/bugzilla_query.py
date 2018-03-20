#! /usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import json
import os
# Python 2/3 compatibility
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

def main():
    nested_dict = lambda: collections.defaultdict(nested_dict)

    # Get absolute path of ../sources from current script location (not current folder)
    sources_folder = os.path.abspath(
                        os.path.join(os.path.dirname( __file__ ),
                        os.pardir,
                        'sources')
                    )
    output_filename = os.path.join(sources_folder, 'bugzilla_components.json')
    json_components = nested_dict()

    # Get list of locales for field cf_locale, used for example on www.mozilla.org
    # Unescaped URL: https://bugzilla.mozilla.org/jsonrpc.cgi?method=Bug.fields&params=[ { 'names': ['cf_locale'] } ]
    json_url = 'https://bugzilla.mozilla.org/jsonrpc.cgi?method=Bug.fields&params=%5B%20{%20%22names%22:%20%5B%22cf_locale%22%5D%20}%20%5D'
    try:
        response = urlopen(json_url)
        json_data = json.load(response)
        try:
            for component in json_data['result']['fields'][0]['values']:
                locale = component['name'].partition('/')[0].strip()
                json_components['cf_locale'][locale] = (
                    {
                        'full_name': component['name'],
                        'description': component['name'].partition('/')[2].strip()
                    }
                )

        except Exception as e:
            print('Error extracting data from json response')
            print(e)
    except Exception as e:
        print('Error reading json reply from {}'.format(json_url))
        print(e)

    # Get list of components of the Mozilla Localizations product
    # Unescaped URL: https://bugzilla.mozilla.org/jsonrpc.cgi?method=Product.get&params=[ { 'names': ['Mozilla Localizations'] } ]
    json_url = 'https://bugzilla.mozilla.org/jsonrpc.cgi?method=Product.get&params=[%20{%20%22names%22:%20[%22Mozilla%20Localizations%22]%20}%20]'
    try:
        response = urlopen(json_url)
        json_data = json.load(response)
        try:
            for component in json_data['result']['products'][0]['components']:
                locale = component['name'].partition('/')[0].strip()
                excluded_components = [
                    'Documentation', 'Infrastructure',
                    'Other', 'Registration & Management'
                ]
                if not locale in excluded_components:
                    json_components['mozilla_localizations'][locale] = (
                        {
                            'full_name': component['name'],
                            'description': component['name'].partition('/')[2].strip()
                        }
                    )

        except Exception as e:
            print('Error extracting data from json response')
            print(e)
    except Exception as e:
        print('Error reading json reply from {}'.format(json_url))
        print(e)

    # Write list of components name
    cache_file = open(output_filename, 'w')
    cache_file.write(json.dumps(json_components, sort_keys=True, indent=2))
    cache_file.close()


if __name__ == '__main__':
    main()
