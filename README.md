mozilla-l10n-query
==================

Web service to provide data like supported locales for a product or Gaia version, supported Gaia versions, etc.

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

Default is to display component names for the ```Mozilla Localizations```product.
If XXX is set to ```www``` display values of the *Locale* select (```cf_locale``` field) used for example in www.mozilla.org::L10N
