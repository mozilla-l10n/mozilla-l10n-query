#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from urllib.parse import quote as urlquote
from urllib.request import urlopen


def saveTextFile(sources_folder, filename, locales, subfolder=''):
    print('Writing file {}.txt'.format(filename))
    if subfolder != '':
        sources_folder = os.path.join(sources_folder, subfolder)
    output_file = open(os.path.join(sources_folder, '{}.txt'.format(filename)), 'w')
    for locale in locales:
        output_file.write('{}\n'.format(locale))
    output_file.close()


def main():
    update_sources = {
        'central': {
            'sources': [
                'https://hg.mozilla.org/mozilla-central/raw-file/default/browser/locales/all-locales',
            ],
            'filename': 'central',
            'format': 'txt',
            'gecko_strings': True,
        },
        'beta': {
            'sources': [
                'https://hg.mozilla.org/releases/mozilla-beta/raw-file/default/browser/locales/shipped-locales',
            ],
            'filename': 'beta',
            'format': 'txt',
            'gecko_strings': True,
        },
        'release': {
            'sources': [
                'https://hg.mozilla.org/releases/mozilla-release/raw-file/default/browser/locales/shipped-locales',
            ],
            'filename': 'release',
            'format': 'txt',
            'gecko_strings': True,
        },
    }

    # Get absolute path of ../sources from current script location (not current folder)
    sources_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'sources'))

    # Gecko-strings channel is a special repository including all locales
    # shipping across all the branches. It also includes en-US
    gecko_strings_locales = []

    # Query Pontoon API to find locales supported in desktop products and
    # mozilla.org
    pontoon_locales = {
        'pontoon': [],
        'pontoon-mozorg': [],
    }

    query = '''
{
  firefox: project(slug: "firefox") {
    ...allLocales
  }
  firefox_ios: project(slug: "firefox-for-ios") {
    ...allLocales
  }
  mozilla_org: project(slug: "mozillaorg") {
    ...allLocales
  }
  android_l10n_fenix: project(slug: "firefox-for-android") {
    ...allLocales
  }
  android_l10n_lockwise: project(slug: "lockwise-for-android") {
    ...allLocales
  }
  vpn_client: project(slug: "mozilla-vpn-client") {
    ...allLocales
  }
}

fragment allLocales on Project {
  localizations {
    locale {
      code
    }
  }
}
'''
    try:
        url = 'https://pontoon.mozilla.org/graphql?query={}'.format(urlquote(query))
        print('Reading sources for Pontoon')
        response = urlopen(url)
        json_data = json.load(response)
        for project, project_data in json_data['data'].items():
            pontoon_bucket = 'pontoon-mozorg' if project == 'mozilla_org' else 'pontoon'
            for element in project_data['localizations']:
                code = element['locale']['code']
                if code not in pontoon_locales[pontoon_bucket]:
                    pontoon_locales[pontoon_bucket].append(code)

        # Store locales for projects in Pontoon
        projects = list(json_data['data'].keys())
        output = {}
        for project in projects:
            # Ignore Firefox, since the list is coming from hg
            if project == 'firefox':
                continue

            # Need to group different projects for android-l10n
            project_dest = "android_l10n" if project.startswith("android_l10n") else project

            locales = []
            for element in json_data['data'][project_dest]['localizations']:
                locales.append(element['locale']['code'])
            locales.sort()

            if project_dest not in output:
                output[project_dest] = locales
            else:
                output[project_dest] = list(set(output[project_dest] + locales))

            saveTextFile(sources_folder, project_dest, locales)
    except Exception as e:
        print(e)

    for filename, locales in pontoon_locales.items():
        locales.sort()
        saveTextFile(sources_folder, filename, locales, 'tools')

    for id, update_source in update_sources.items():
        supported_locales = []
        for url in update_source['sources']:
            print('Reading sources for {} from {}'.format(id, url))
            response = urlopen(url)
            if update_source['format'] == 'txt':
                for locale in response:
                    locale = locale.rstrip().decode()
                    if locale not in ['', 'en-US'] and locale not in supported_locales:
                        supported_locales.append(locale)
            else:
                json_data = json.load(response)
                for locale in json_data:
                    locale = locale.rstrip()
                    if locale != '' and locale not in supported_locales:
                        supported_locales.append(locale)
        # Sort locales
        supported_locales.sort()
        if update_source['gecko_strings']:
            gecko_strings_locales += supported_locales

        # Write back txt file
        saveTextFile(sources_folder, update_source['filename'], supported_locales)

    # Output gecko-strings locales
    gecko_strings_locales = list(set(gecko_strings_locales))
    gecko_strings_locales.append('en-US')
    gecko_strings_locales.sort()
    saveTextFile(sources_folder, 'gecko_strings', gecko_strings_locales)


if __name__ == '__main__':
    main()
