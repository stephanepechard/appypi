.. _technical-label:

Some technical details
======================

Commands
--------
You may have noticed that appypi commands were almost the same as in
`aptitude <http://packages.debian.org/stable/main/aptitude>`_ , the
`Debian <http://debian.org>`_ packages manager. It is not done unpurposely.
Actually, you can find the same `install`, `remove`, `update` and `upgrade`
in aptitude. The `list` command is not available in aptitude but in
`dpkg <http://packages.debian.org/stable/main/dpkg>`_
The `show` command is not available in aptitude but in
`apt-get <http://packages.debian.org/stable/main/apt>`_.


What does appypi create on your disk?
-------------------------------------
Except for the launchers, everything appypi will create on your disk is confined
to the `.appypi` directory.

Global directory
^^^^^^^^^^^^^^^^
That directory contains all files and directories appypi need to work properly:
 * the appypi database (SQLite format) ;
 * the Pypi packages list dump file ;
 * the appypi cache directory ;
 * for each installed app, a directory containing the `bootstrap` file, the current
   freeze state of the app virtualenv put in the `freeze.txt` and the virtualenv
   in itself put in the `venv` directory.

Launchers
^^^^^^^^^
For each app installed, any launchable script located in the package is translated
by appypi as a launchable script. Any of these file is situated in the user `bin`
directory. It creates it if it does not exist.


Caches
------

Pypi packages list
^^^^^^^^^^^^^^^^^^
You don't want to query the list of **ALL** Pypi packages at the installation
of any package. That's why appypi uses a cache of this Pypi list, to be fast
at installing several packages in a short interval. This cache is written
on disk in a single file, using `Python's pickle functionnalitie
<http://docs.python.org/2/library/pickle.html>`_

Of course, Pypi packages list grows over time, and appypi should keep it up
to date. It is done automatically if the list file is more than 7 days old.
At the moment, there is no way of modifying this duration, but it seems
reasonable. If this does not suit you, you can manually trigger the update
with a simple::

    $ appypi update


Packages cache
^^^^^^^^^^^^^^
appypi maintains its own local cache for Pypi packages. It may be redundant
with your own pip cache if you set it already (and you should), but this way
appypi is kept independent from pip. Then, each single package comes
either directly from Pypi or from the appypi local cache.

The annoying thing is that if pip find a package in the cache, it
asks the user what to do with it::

    The file /home/user/.appypi/appypi_cache/glances-1.5.1.tar.gz exists. (i)gnore, (w)ipe, (b)ackup

There is no way to tell pip what to do programmatically before its version 1.3.
For previous versions of pip, you have to manually choose **(i)gnore** anytime
it is asked. Shitty, I know...

In case it is too disturbing for you, you can delete the full cache with::

    $ rm -rf ~/.appypi/appypi_cache


Slowness?
---------
As you can imagine, entering in  a virtualenv for each command is a bit
time-consuming. Your package may therefore be take a little more time to start
than usually. It is therefore not recommended to use appypi with particularly
time-sensitive usage. For any other use of common packages,
appypi is the way to go :-)

