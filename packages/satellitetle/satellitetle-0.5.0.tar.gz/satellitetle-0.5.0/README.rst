============
satellitetle
============

The python package satellitetle_ provides functions to fetch TLEs from
various online sources (currently CelesTrak, CalPoly and AMSAT).

It was forked from the python package orbit_.

.. _satellitetle: https://gitlab.com/librespacefoundation/python-satellitetle
.. _orbit: http://github.com/seanherron/orbit


Usage
-----

Fetch TLEs for a single satellite from Celestrak:
::

 from satellite_tle import fetch_tle_from_celestrak

 norad_id_iss = 25544 # ISS (ZARYA)
 print(fetch_tle_from_celestrak(norad_id_iss))

Fetch a large set of TLEs for a list of satllites from all available sources:
::

 from satellite_tle import fetch_tles

 norad_ids = [25544, # ISS (ZARYA)
              4298,  # QIKCOM-1
              40379] # GRIFEX

 tles = fetch_tles(norad_ids)

 for norad_id, (source, tle) in tles.items():
     print('{:5d} {:23s}: {:23s}'.format(norad_id, tle[0], source))

NOTE: `fetch_tles` downloads the TLE sets from all known sources (>40 urls),
so it should only be used when fetching TLEs for a large set of satellites.

Another usage example is given in `example_fetchall.py`.

License
-------

MIT
