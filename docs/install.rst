.. _install-label:

Installation instructions
=========================
It is usually suggested to install a package like appypi in a
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_. It is still possible
here, but it is recommended to use the *meta-style* installation process.

Meta-style
----------
As appypi is an app installer, you can use it to install itself.
This way, your installation is consistent and you keep everything
in the dedicated database. Here is a little script to do this in one shot.
You need at least pip version 0.8.1 to do that::

	virtualenv -q /tmp/appypi-venv &&
	source /tmp/appypi-venv/bin/activate &&
	pip -q install appypi &&
	appypi install appypi &&
	deactivate

After that, you can begin to :ref:`use appypi <usage-label>`, as it is
callable in your PATH.


Usual suspects: pip and distribute
----------------------------------
To install appypi for your user only, type::

    $ pip install projy --user

To install appypi system-wide, just type::

    $ sudo pip install projy

If no pip available, try ``easy_install``::

    $ sudo easy_install projy


Play the game
-------------
If you want to code, hack, enhance or just understand appypi, you can get
the latest code at `Github <http://github.com/stephanepechard/appypi>`_::

    $ git clone http://github.com/stephanepechard/appypi

Then create the local virtualenv and install appypi::

    $ cd appypi && source bootstrap && fab install
