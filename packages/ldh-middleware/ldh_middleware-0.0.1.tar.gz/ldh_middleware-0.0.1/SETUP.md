Prerequisites
-------------

* Debian 9
* Python 3.5
* Django 1.11 (included in Python packages below)
* Nginx
* RabbitMQ server
    * Must be accessible at `amqp://guest:guest@localhost:5672//`
    * This can be achieved with just `apt install rabbitmq-server`
* Additional dependencies (Debian package names):
    * `libsasl2-dev`
    * `libldap2-dev`
    * `libssl-dev`
    * `python3-dev`
    * `supervisor`
    * `uwsgi`
    * `uwsgi-emperor`
    * `uwsgi-plugin-python3`
    * `virtualenv`
* Python/Django dependencies: see `requirements.txt`
* External resources:
    * LDAP database
    * WooCommerce instance
      * [REST API enabled](https://docs.woocommerce.com/document/woocommerce-rest-api/)
      * [WooCommerce Subscriptions](https://woocommerce.com/products/woocommerce-subscriptions/)
      * [JWT Authentication for WP REST API](https://wordpress.org/plugins/jwt-authentication-for-wp-rest-api/)
    * OpenVPN instance (SSH access)
      * Including [openvpn-confgen](https://code.puri.sm/liberty/openvpn_confgen)
      * Typically, the Nginx user (`www-data`) will need SSH access
      * Test with `sudo -u www-data ssh -p PORT REMOTE_USER@HOSTNAME`
      * The user needing access can be changed in
        `purist_middleware_monitor.conf`

Other versions and alternatives may work but are untested.

Setup
-----

* Install Debian packages (`apt install libsasl2-dev libldap2-dev...`)
* Create installation folders:
    * `/opt/purist/middleware/` (code)
    * `/opt/purist/middleware_virtualenv/` (Python environment)
    * `/etc/opt/purist/middleware/` (configuration)
    * `/var/opt/purist/middleware/static/` (data and static web files)
    * `/var/log/purist/middleware/` (logs)
* Populate brand data (if it doesn't already exist):
    * Create `/var/opt/purist/brand/` (shared data and static web files)
    * Populate `brand` folder
    * `chown --recursive www-data:www-data /var/opt/purist`
* Copy project code:
    * Copy code into `/opt/purist/middleware/`
    * `chown --recursive www-data:www-data /opt/purist`
* Set up virtualenv:
    * Create virtualenv (`virtualenv /opt/purist/middleware_virtualenv --python=python3`)
    * `cd /opt/purist/middleware`
    * Activate virtualenv (`source ../account_virtualenv/bin/activate`)
    * Install Python packages (`pip install --requirement requirements.txt`)
    * Confirm packages by comparing `pip freeze` output with `requirements.txt`
    * Deactivate virtualenv (`deactivate`)
* Complete Django settings:
    * `cp ./conf/etc/config.ini /etc/opt/purist/middleware/`
    * `cp ./conf/etc/secret.ini /etc/opt/purist/middleware/`
    * Fill in settings
* Run initial setup:
    * Activate virtualenv (`source ../account_virtualenv/bin/activate`)
    * `./manage.py collectstatic`
    * `./manage.py migrate`
    * `./manage.py createsuperuser`
    * When prompted, enter the credentials of your LDAP superuser /
      account manager
    * Deactivate virtualenv (`deactivate`)
* Hook up Nginx:
    * `cp ./config/nginx/purist_middleware /etc/nginx/available_sites/`
    * Update `server_name` value
    * `cd /etc/nginx/sites-enabled`
    * `ln --symbolic ../sites-available/purist_middleware`
* Hook up uWSGI:
    * `sudo apt install uwsgi uwsgi-emperor uwsgi-plugin-python3`
    * `cp ./conf/uwsgi_emperor_vassals/purist_middleware.ini /etc/uwsgi-emperor/vassals/`
* Hook up Supervisor (supervisord):
    * `sudo apt install supervisor`
    * `cp ./conf/supervisord/purist_middleware_monitor.conf /etc/supervisor/conf.d/`
* Restart services:
    * `sudo service rabbitmq-server restart`
    * `sudo service uwsgi-emperor restart`
    * `sudo service nginx restart`
    * `sudo service supervisor restart`
* Check logs:
    * `/var/log/nginx/access.log`
    * `/var/log/nginx/error.log`
    * `/var/log/purist/middleware/beat.log`
    * `/var/log/supervisor/supervisord.log`
    * `/var/log/uwsgi/emperor.log`
    * `/var/log/uwsgi/app/purist_middleware.log`

For more options and details see
<https://docs.djangoproject.com/en/1.11/#the-development-process>

Configure
---------

* Log in to admin interface as superuser
* Define intervals in Django_Celery_Beat > Intervals
* Define periodic tasks in Django_Celery_Beat > Periodic tasks
* Define known products in Limit Monitor > External bundles

Update
------

* Stop site
* Update packages with `apt update && apt upgrade`
* Update code in `/opt/purist/middleware/`
* Update settings in `/etc/opt/purist/middleware/`
* Update virtualenv:
    * Activate virtualenv (`./bin/activate.py`)
    * Update Python packages (`pip install  --requirement requires/requirements.txt`)
    * Do not use `pip install --update` as this will not respect requirements
* Update site:
    * Run `./manage.py collectstatic`
    * Run `./manage.py migrate` (see **Migrations** below)
* Start site

Migrations
----------

This is a workaround for [django-ldapdb issue #155](https://github.com/django-ldapdb/django-ldapdb/issues/115).

If you need to make a new migration:

* Open `ldapregister.0003_ldapgroup_ldapperson`
* Switch `LdapGroup.cn` and `LdapPerson.uid` from non-primary to primary
* Run `makemigrations`
* Switch `LdapGroup.cn` and `LdapPerson.uid` back to non-primary
* If you have just added a new LDAP table, switch `NewTable.key` to
  non-primary too
* Run `migrate`

You only need to do this when creating new migrations (`makemigrations`)
not when running existing migrations (`migrate`).

Usage
-----

See [README.md](README.md)
