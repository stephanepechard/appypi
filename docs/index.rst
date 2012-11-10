.. _index-label:

appypi: sandboxing apps from Pypi packages
==========================================
**appypi** is a terminal-based `Python Package Index`_ package manager.
Each app installed through appypi is sandboxed in an individual virtualenv
and usable from the user space. No root access is required to install an app.
appypi in **NOT** a replacement for pip_ or easy_install_.
Actually, it uses pip intensively to manage package installations.

appypi creates launchers into the user ~/bin directory. These launchers mimic
the package behavior in terms of what commands can be called. For example,
appypi will create a *django-admin.py* launcher when installing the
django_ package, and a *fab* launcher when installing the Fabric_ package.
This way, you can use the package as if it was installed with pip directly.

appypi won't install a package if it finds it in your path already.
It is your duty to take care of these external installations before using appypi.

.. _`Python Package Index`: http://pypi.python.org/pypi
.. _pip: http://www.pip-installer.org/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall
.. _Fabric: http://fabfile.org/
.. _django: http://djangoproject.com/


Installing a package::

    $ appypi install django
    Looking for django...
    Found Django version 1.4.2
    Installing...
    Install successful!

Upgrading a package::

    $ appypi upgrade django
    Upgrading: Django (1.3 => 1.4.2)

Removing a package::

    $ appypi remove django
    These packages will be REMOVED:

        Django

    Do you want to continue? [y/n]y
    Package Django has been removed.



.. toctree::
    :maxdepth: 2

    install
    usage
    technical
    changelog
