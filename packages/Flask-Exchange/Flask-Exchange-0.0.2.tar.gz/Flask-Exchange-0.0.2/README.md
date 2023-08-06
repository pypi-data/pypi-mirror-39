Flask-Exchange
==============
Flask-Exchange is a simple and basic Flask extension which adds support for the Exchange using ExchangeLib.
This extension is still in development and does not cover all setups for exchangelib.
Even with its current limited functionality, it still might be useful for most users.

TODO for next release
===============
- develop API for sending, getting and finding mail (and other items).
- use APScheduler for fetching mail (exchangelib push currently not finished).


Doc
===============
look at the examples_ to see how to set it up in your Flask app. 
If you need to know how to use the ExchangeLib API then please look at the authors page:
https://github.com/ecederstrand/exchangelib

Requirements
===============

	Python > 3.6
	Flask > 0.10.1
	ExchangeLib > 1.12.0

Install
===============
You can install Flask-Exchange via Python Package Index (PyPI_),::

    $ pip install Flask-Exchange

Contribution
===============
Please use the Issues_ for feature requests & troubleshooting.