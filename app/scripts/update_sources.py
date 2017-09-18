#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import urllib2

def main():
    update_sources = {
        'central' : {
            'sources': [
                'http://hg.mozilla.org/mozilla-central/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/mozilla-central/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'central.txt',
            'format': 'txt',
            'cross': True,
        },
        'beta' : {
            'sources': [
                'http://hg.mozilla.org/releases/mozilla-beta/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/releases/mozilla-beta/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'beta.txt',
            'format': 'txt',
            'cross': True,
        },
        'release' : {
            'sources': [
                'http://hg.mozilla.org/releases/mozilla-release/raw-file/default/browser/locales/all-locales',
                'http://hg.mozilla.org/releases/mozilla-release/raw-file/default/mobile/android/locales/all-locales',
            ],
            'filename': 'release.txt',
            'format': 'txt',
            'cross': True,
        },
        'firefox_ios' : {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=firefox-ios&txt',
            ],
            'filename': 'firefox_ios.txt',
            'format': 'txt',
            'cross': False,
        },
        'focus_ios' : {
            'sources': [
                'https://l10n.mozilla-community.org/webstatus/api/?product=focus-ios&txt',
            ],
            'filename': 'focus_ios.txt',
            'format': 'txt',
            'cross': False,
        },
        'mozilla.org' : {
            'sources': [
                'https://l10n.mozilla-community.org/langchecker/?action=listlocales&website=0&json',
            ],
            'filename': 'mozilla_org.txt',
            'format': 'json',
            'cross': False,
        },
    }

    # Get absolute path of ../sources from current script location (not current folder)
    sources_folder = os.path.abspath(
                        os.path.join(os.path.dirname( __file__ ),
                        os.pardir,
                        'sources')
                    )

    # Cross channel is a special repository including all locales shipping
    # across all the branches. It also includes en-US
    cross_locales = []

    for id, update_source in update_sources.iteritems():
        supported_locales = []
        for url in update_source['sources']:
            print 'Reading sources for {0} from {1}'.format(id, url)
            response = urllib2.urlopen(url)
            if update_source['format'] == 'txt':
                for locale in response:
                    if locale != '' and locale not in supported_locales:
                        supported_locales.append(locale)
            else:
                json_data = json.load(response)
                for locale in json_data:
                    if locale != '' and locale not in supported_locales:
                        supported_locales.append(locale + '\n')
        # Sort locales
        supported_locales.sort()
        if update_source['cross']:
            cross_locales += supported_locales

        # Write back txt file
        print 'Writing file', update_source['filename']
        output_file = open(os.path.join(sources_folder, update_source['filename']), 'w')
        for locale in supported_locales:
            output_file.write(locale)
        output_file.close()

    # Output cross locales
    cross_locales = list(set(cross_locales))
    cross_locales.append('en-US\n')
    cross_locales.sort()
    print 'Writing file cross.txt'
    output_file = open(os.path.join(sources_folder, 'cross.txt'), 'w')
    for locale in cross_locales:
        output_file.write(locale)
    output_file.close()

if __name__ == '__main__':
    main()
