#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import toml
from urllib.parse import quote as urlquote
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

    all_locales = []

    query = """
{
  firefox: project(slug: "firefox") {
    ...allLocales
  }
  thunderbird: project(slug: "thunderbird") {
    ...allLocales
  }
  seamonkey: project(slug: "seamonkey") {
    ...allLocales
  }
  firefox_ios: project(slug: "firefox-for-ios") {
    ...allLocales
  }
  firefox_com: project(slug: "firefoxcom") {
    ...allLocales
  }
  mozilla_org: project(slug: "mozillaorg") {
    ...allLocales
  }
  android_l10n_fenix: project(slug: "firefox-for-android") {
    ...allLocales
  }
  android_l10n_focus: project(slug: "focus-for-android") {
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
"""
    try:
        url = f"https://pontoon.mozilla.org/graphql?query={urlquote(query)}&raw"
        print("Reading sources for Pontoon")
        response = urlopen(url)
        json_data = json.load(response)
        for project, project_data in json_data["data"].items():
            pontoon_bucket = (
                "pontoon-mozorg"
                if project in ["firefox_com", "mozilla_org"]
                else "pontoon"
            )
            for element in project_data["localizations"]:
                code = element["locale"]["code"]
                if code not in pontoon_locales[pontoon_bucket]:
                    pontoon_locales[pontoon_bucket].append(code)

        # Store locales for projects in Pontoon
        projects = list(json_data["data"].keys())
        output = {}
        for project in projects:
            # Ignore Firefox, since the list is coming from hg
            if project == "firefox":
                continue

            # Need to group different projects for android-l10n
            project_dest = (
                "android_l10n" if project.startswith("android_l10n") else project
            )

            locales = []
            for element in json_data["data"][project]["localizations"]:
                locales.append(element["locale"]["code"])

            """
            For mozilla.org, need to take into account locales not enabled in
            Pontoon but in Smartling, available in a TOML file.
            """
            if project == "mozilla_org":
                url = "https://raw.githubusercontent.com/mozilla-l10n/www-l10n/master/configs/vendor.toml"
                response = urlopen(url).read()
                parsed_toml = toml.loads(response.decode("utf-8"))
                locales += parsed_toml["locales"]
            if project == "firefox_com":
                url = "https://raw.githubusercontent.com/mozilla-l10n/www-l10n/master/configs/vendor.toml"
                response = urlopen(url).read()
                parsed_toml = toml.loads(response.decode("utf-8"))
                locales += parsed_toml["locales"]

            # Manually add extra locales not available in Pontoon for some projects
            if project in ["thunderbird", "seamonkey"]:
                locales.append("ja")

            if project_dest not in output:
                output[project_dest] = locales
            else:
                output[project_dest] = list(set(output[project_dest] + locales))

        # Save to file
        for project, locales in output.items():
            locales.sort()
            # Save list of locales across projects
            all_locales = locales + all_locales
            saveTextFile(sources_folder, project, locales)
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
