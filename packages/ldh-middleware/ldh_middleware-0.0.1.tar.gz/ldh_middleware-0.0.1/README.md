Keel
====

[project] | [code] | [tracker]

A Django-based middleware application (with a user-facing web interface)
for managing services, resources and subscription-based accounts on a
Liberty Deckplan Host (LDH). The reference implementation for LDH
middleware. Tailored for services operated by Purism SPC, but ready to
be modified and deployed anywhere, by anyone.

Installation
------------

Follows an opinionated installation process (specifically expecting
one-instance-per-server), but includes a number of configuration
options.

See [SETUP.md] for prerequisites and instructions.

Usage
-----

* Start Django site as a system service, or with `./manage.py runserver`
* Visit <https://example.com> and follow the login or registration
  links.
  * If registration is closed, you will have to create LDAP credentials
    another way.
* Manage user profile at <https://example.com/accounts/profile/>

Models
------

![Database model diagram](models.png)

Model diagram generated with:

    ./manage.py graph_models --all-applications --group-models \
    --verbose-name --output models.png

Build
-----

Follow these instructions to build LDH as a Python package:

```
  $ apt-get install git
  $ apt-get install libsasl2-dev libldap2-dev libssl-dev python3-dev supervisor uwsgi uwsgi-emperor uwsgi-plugin-python3 virtualenv gcc pipenv
  $ git clone https://source.puri.sm/liberty/ldh_middleware.git
  $ cd ldh_middleware
  $ pipenv install --dev
  $ pipenv shell
  $ python setup.py sdist bdist_wheel
```

If everything works as expected you should end up with the files:

* `ldh_middleware-<version>-py3-none-any.whl`
* `ldh_middleware-<version>.tar.gz`

under dist/ directory.

Sharing and contributions
-------------------------

Keel (LDH middleware)  
<https://source.puri.sm/liberty/ldh_middleware>  
Copyright 2017-2018 Purism SPC  
SPDX-License-Identifier: AGPL-3.0-or-later

Shared under AGPL-3.0-or-later. We adhere to the Community Covenant
1.0 without modification, and certify origin per DCO 1.1 with a
signed-off-by line. Contributions under the same terms are welcome.

For details see:

* [COPYING.md], license notices
* [COPYING.AGPL.md], full license text
* [CODE_OF_CONDUCT.md], full conduct text
* [CONTRIBUTING.DCO.md], full origin text

<!-- * [CONTRIBUTING.md], additional contribution notes -->

<!-- Links -->

[project]: https://source.puri.sm/liberty/ldh_middleware
[code]: https://source.puri.sm/liberty/ldh_middleware/tree/master
[tracker]: https://source.puri.sm/liberty/ldh_middleware/issues
[SETUP.md]: SETUP.md
[COPYING.AGPL.md]: COPYING.AGPL.md
[CODE_OF_CONDUCT.md]: CODE_OF_CONDUCT.md
[CONTRIBUTING.DCO.md]: CONTRIBUTING.DCO.md
[COPYING.md]: COPYING.md
[CONTRIBUTING.md]: CONTRIBUTING.md
