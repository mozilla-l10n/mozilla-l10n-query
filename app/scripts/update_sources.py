#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
# Python 2/3 compatibility
try:
    from urllib import quote_plus as urlquote
except ImportError:
    from urllib.parse import quote as urlquote
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    dict.iteritems
except AttributeError:
    # Python 3
    def iteritems(d):
        return iter(d.items())
else:
    # Python 2
    def iteritems(d):
        return d.iteritems()


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
                'https://hg.mozilla.org/mozilla-central/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'central',
            'format': 'txt',
            'gecko_strings': True,
        },
        'beta': {
            'sources': [
                'https://hg.mozilla.org/releases/mozilla-beta/raw-file/default/browser/locales/shipped-locales',
                'https://hg.mozilla.org/releases/mozilla-beta/raw-file/default/mobile/android/locales/maemo-locales',
            ],
            'filename': 'beta',
            'format': 'txt',
            'gecko_strings': True,
        },
        'release': {
            'sources': [
                'https://hg.mozilla.org/releases/mozilla-release/raw-file/default/browser/locales/shipped-locales',
                'https://hg.mozilla.org/releases/mozilla-release/raw-file/default/mobile/android/locales/maemo-locales',
            ],
            'filename': 'release',
            'format': 'txt',
            'gecko_strings': True,
        },
        'firefox_ios': {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=firefox-ios&txt',
            ],
            'filename': 'firefox_ios',
            'format': 'txt',
            'gecko_strings': False,
        },
        'mozilla.org': {
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
  fennec: project(slug: "firefox-for-android") {
    ...allLocales
  }
  mozillaorg: project(slug: "mozillaorg") {
    ...allLocales
  }
  androidl10n: project(slug: "android-l10n") {
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
        for project, project_data in iteritems(json_data['data']):
            pontoon_bucket = 'pontoon-mozorg' if project == 'mozillaorg' else 'pontoon'
            for element in project_data['localizations']:
                code = element['locale']['code']
                if code not in pontoon_locales[pontoon_bucket]:
                    pontoon_locales[pontoon_bucket].append(code)

        # Store android-l10n
        android_locales = []
        for element in json_data['data']['androidl10n']['localizations']:
            android_locales.append(element['locale']['code'])
        android_locales.sort()
        saveTextFile(sources_folder,
                     'android_l10n', android_locales)

    except Exception as e:
        print(e)

    for filename, locales in iteritems(pontoon_locales):
        locales.sort()
        saveTextFile(sources_folder, filename, locales, 'tools')

    for id, update_source in iteritems(update_sources):
        supported_locales = []
        for url in update_source['sources']:
            print('Reading sources for {} from {}'.format(id, url))
            response = urlopen(url)
            if update_source['format'] == 'txt':
                for locale in response:
                    locale = locale.rstrip().decode()
                    if 'shipped-locales' in url:
                        # Remove platform from shipped-locales
                        for text in ['linux', 'osx', 'win32']:
                            locale = locale.replace(text, '').rstrip()
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
