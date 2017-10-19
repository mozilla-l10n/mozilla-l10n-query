#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import urllib
import urllib2
import sys


def saveTextFile(sources_folder, filename, locales, subfolder = ''):
    print('Writing file {}.txt'.format(filename))
    if subfolder != '':
        sources_folder = os.path.join(sources_folder, subfolder)
    output_file = open(os.path.join(sources_folder, '{}.txt'.format(filename)), 'w')
    for locale in locales:
        output_file.write(locale + '\n')
    output_file.close()


def main():
    update_sources = {
        'central' : {
            'sources': [
                'http://hg.mozilla.org/mozilla-central/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/mozilla-central/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'central',
            'format': 'txt',
            'gecko_strings': True,
        },
        'beta' : {
            'sources': [
                'http://hg.mozilla.org/releases/mozilla-beta/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/releases/mozilla-beta/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'beta',
            'format': 'txt',
            'gecko_strings': True,
        },
        'release' : {
            'sources': [
                'http://hg.mozilla.org/releases/mozilla-release/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/releases/mozilla-release/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'release',
            'format': 'txt',
            'gecko_strings': True,
        },
        'firefox_ios' : {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=firefox-ios&txt',
            ],
            'filename': 'firefox_ios',
            'format': 'txt',
            'gecko_strings': False,
        },
        'focus_android' : {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=focus-android&txt',
            ],
            'filename': 'focus_android',
            'format': 'txt',
            'gecko_strings': False,
        },
        'focus_ios' : {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=focus-ios&txt',
            ],
            'filename': 'focus_ios',
            'format': 'txt',
            'gecko_strings': False,
        },
        'mozilla.org' : {
            'sources': [
                'https://l10n.mozilla-community.org/langchecker/?action=listlocales&website=0&json',
            ],
            'filename': 'mozilla_org',
            'format': 'json',
            'gecko_strings': False,
        },
    }

    # Get absolute path of ../sources from current script location (not current folder)
    sources_folder = os.path.abspath(
                        os.path.join(os.path.dirname( __file__ ),
                        os.pardir,
                        'sources')
                    )

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
  fennec: project(slug: "firefox-for-android") {
    ...allLocales
  }
  mozillaorg: project(slug: "mozillaorg") {
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
''';
    try:
        url = 'https://pontoon.mozilla.org/graphql?query={}'.format(urllib.quote_plus(query))
        print('Reading sources for Pontoon')
        response = urllib2.urlopen(url)
        json_data = json.load(response)
        for project, project_data in json_data['data'].iteritems():
            if project == 'mozillaorg':
                for element in project_data['localizations']:
                    code = element['locale']['code']
                    if code not in pontoon_locales['pontoon-mozorg']:
                        pontoon_locales['pontoon-mozorg'].append(code)
            else:
                for element in project_data['localizations']:
                    code = element['locale']['code']
                    if code not in pontoon_locales['pontoon']:
                        pontoon_locales['pontoon'].append(code)
    except Exception as e:
        print(e)

    for filename, locales in pontoon_locales.iteritems():
        locales.sort()
        saveTextFile(sources_folder, filename, locales, 'tools')

    for id, update_source in update_sources.iteritems():
        supported_locales = []
        for url in update_source['sources']:
            print('Reading sources for {} from {}'.format(id, url))
            response = urllib2.urlopen(url)
            if update_source['format'] == 'txt':
                for locale in response:
                    locale = locale.rstrip()
                    if locale != '' and locale not in supported_locales:
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
