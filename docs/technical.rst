.. _technical-label:

Some technical details
======================

Caches
------

Pypi packages list
++++++++++++++++++
You don't want to query the list of **ALL** Pypi packages at the installation
of any package. That's why appypi uses a cache of this Pypi list, to be fast
at installing several packages in a short interval. This cache is written
on disk in a single file, using `Python's pickle functionnalities`_.

Of course, Pypi packages list grows over time, and appypi should keep it up
to date. It is done automatically if the list file is more than 7 days old.
At the moment, there is no way of modifying this duration, but it seems
reasonable. If this does not suit you, you can manually trigger the update
with a simple::

    $ appypi update

.. _`Python's pickle functionnalities`: http://docs.python.org/2/library/pickle.html


Packages cache
++++++++++++++
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

