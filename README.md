mozilla-l10n-query
==================

Web service to provide data like supported locales for a product, Bugzilla component names, and more.

## Installation
Install [Composer](https://getcomposer.org/) and its dependencies.

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

```
/?tool=XXX
```
Display list of locales working in a specific tool. Available values: pontoon, pontoon-mozorg, all.

`all` will return a json with the list of supported tools and, for each of them, the supported locales.


# License
This software is released under the terms of the [Mozilla Public License v2.0](http://www.mozilla.org/MPL/2.0/).
