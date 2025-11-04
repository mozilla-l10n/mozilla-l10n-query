#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import toml
from urllib.request import urlopen


def saveTextFile(sources_folder, filename, locales, subfolder=""):
    print("Writing file {}.txt".format(filename))
    if subfolder != "":
        sources_folder = os.path.join(sources_folder, subfolder)
    output_file = open(os.path.join(sources_folder, "{}.txt".format(filename)), "w")
    for locale in locales:
        output_file.write("{}\n".format(locale))
    output_file.close()


def main():
    update_sources = {
        "central": {
            "sources": [
                "https://raw.githubusercontent.com/mozilla-firefox/firefox/refs/heads/main/browser/locales/all-locales",
            ],
            "filename": "central",
            "format": "txt",
            "gecko_strings": True,
        },
        "beta": {
            "sources": [
                "https://raw.githubusercontent.com/mozilla-firefox/firefox/refs/heads/beta/browser/locales/shipped-locales",
            ],
            "filename": "beta",
            "format": "txt",
            "gecko_strings": True,
        },
        "release": {
            "sources": [
                "https://raw.githubusercontent.com/mozilla-firefox/firefox/refs/heads/release/browser/locales/shipped-locales",
            ],
            "filename": "release",
            "format": "txt",
            "gecko_strings": True,
        },
    }

    # Get absolute path of ../sources from current script location (not current folder)
    sources_folder = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "sources")
    )

    # Gecko-strings channel is a special repository including all locales
    # shipping across all the branches. It also includes en-US
    gecko_strings_locales = []

    # Query Pontoon API to find locales supported in desktop products and
    # mozilla.org
    pontoon_locales = {
        "pontoon": [],
        "pontoon-mozorg": [],
    }

    filename_mapping = {
        "firefox-for-ios": "firefox_ios",
        "firefoxcom": "firefox_com",
        "mozilla-vpn-client": "vpn_client",
        "mozillaorg": "mozilla_org",
    }
    projects = {
        "firefox-for-android": [],
        "firefox-for-ios": [],
        "firefox": [],
        "firefoxcom": [],
        "focus-for-android": [],
        "mozilla-vpn-client": [],
        "mozillaorg": [],
        "seamonkey": [],
        "thunderbird": [],
    }

    all_locales = []
    try:
        url = "https://pontoon.mozilla.org/api/v2/projects/?fields=slug,locales&page_size=1000"
        print("Reading sources for Pontoon")
        response = urlopen(url)
        json_data = json.load(response)

        for project in json_data["results"]:
            slug = project["slug"]
            if slug not in projects:
                continue
            projects[slug] = project["locales"]
            pontoon_bucket = (
                "pontoon-mozorg" if slug in ["firefoxcom", "mozillaorg"] else "pontoon"
            )
            pontoon_locales[pontoon_bucket] = list(
                set(pontoon_locales[pontoon_bucket]) | set(project["locales"])
            )

        # Store locales for projects in Pontoon
        output = {}
        for project, project_locales in projects.items():
            # Ignore Firefox, since the list is coming from the code repository
            if project == "firefox":
                continue

            # Need to group different projects for android-l10n
            project_dest = "android_l10n" if ("android") in project else project

            """
            For mozilla.org, need to take into account locales not enabled in
            Pontoon but in Smartling, available in a TOML file.
            """
            if project == "mozillaorg":
                url = "https://raw.githubusercontent.com/mozilla-l10n/www-l10n/master/configs/vendor.toml"
                response = urlopen(url).read()
                parsed_toml = toml.loads(response.decode("utf-8"))
                project_locales += parsed_toml["locales"]
            if project == "firefoxcom":
                url = "https://raw.githubusercontent.com/mozilla-l10n/www-firefox-l10n/master/configs/vendor.toml"
                response = urlopen(url).read()
                parsed_toml = toml.loads(response.decode("utf-8"))
                project_locales += parsed_toml["locales"]

            # Manually add extra locales not available in Pontoon for some projects
            if project in ["thunderbird", "seamonkey"]:
                project_locales.append("ja")

            if project_dest not in output:
                output[project_dest] = project_locales
            else:
                output[project_dest] = list(set(output[project_dest] + project_locales))

        # Save to file
        for project, locales in output.items():
            locales.sort()
            # Save list of locales across projects
            all_locales = locales + all_locales
            saveTextFile(
                sources_folder, filename_mapping.get(project, project), locales
            )
    except Exception as e:
        sys.exit(e)

    for filename, locales in pontoon_locales.items():
        locales.sort()
        saveTextFile(sources_folder, filename, locales, "tools")

    for id, update_source in update_sources.items():
        supported_locales = []
        for url in update_source["sources"]:
            print("Reading sources for {} from {}".format(id, url))
            response = urlopen(url)
            if update_source["format"] == "txt":
                for locale in response:
                    locale = locale.rstrip().decode()
                    if locale not in ["", "en-US"] and locale not in supported_locales:
                        supported_locales.append(locale)
            else:
                json_data = json.load(response)
                for locale in json_data:
                    locale = locale.rstrip()
                    if locale != "" and locale not in supported_locales:
                        supported_locales.append(locale)
        # Sort locales
        supported_locales.sort()
        if update_source["gecko_strings"]:
            gecko_strings_locales += supported_locales

        # Write back txt file
        saveTextFile(sources_folder, update_source["filename"], supported_locales)

    # Output gecko-strings locales
    gecko_strings_locales = list(set(gecko_strings_locales))
    gecko_strings_locales.append("en-US")
    gecko_strings_locales.sort()
    saveTextFile(sources_folder, "gecko_strings", gecko_strings_locales)

    # Save list of all locales
    all_locales.append("en-US")
    all_locales = list(set(all_locales))
    all_locales.sort()
    saveTextFile(sources_folder, "all_projects", all_locales)


if __name__ == "__main__":
    main()
