mozilla-l10n-query
==================

Web service to provide data like supported locales for a product or Gaia version, supported Gaia versions, etc.

## Installation
Install [Composer](https://getcomposer.org/) and its dependencies.

Run `/app/scripts/bugzilla_query.py` at least once to populate the list of Bugzilla locales. A daily cronjob should be added for this task on a production server. Make sure that the output folder `app/sources` is writable by the user running this script (output file is `bugzilla_components.json`).

## Available URLs
```
/
```
Display all available repositories (ID, name and array of supported locales).


```
/?type=XXX
```
Display all repositories with type XXX (ID, name and array of supported locales).


```
/?repo=XXX
```
Display only the requested repository  (ID, name and array of supported locales).


```
/?bugzilla=XXX
```
Display list of Bugzilla's l10n component names, used to create queries and links in products like Webdashboard or Langchecker.

Default is to display component names for the `Mozilla Localizations` product.
If XXX is set to `www` display values of the *Locale* select (`cf_locale` field) used for example in www.mozilla.org::L10N

# License
This software is released under the terms of the [Mozilla Public License v2.0](http://www.mozilla.org/MPL/2.0/).
