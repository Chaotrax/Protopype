# Unknown Places
The python-script for my Bachelors Thesis "Unknown Places: Automatisierte Identifikation unbekannter Orte aus Kontextinformationen" \
The aim of this Python script is a feasibility study of the implementation of Øyvind Eide's model of identifying unknown locations from contextual information, as presented in _Media Boundaries and conceptual Modelling_ (2013)

### How to use:
After starting main.py, a programme loop leads through the input of the coordinates of the reference locations and their processing form. Alternatively, a csv file can be read in.
Coordinates can be added in WGS84 decimal system or as UTM-coordinates.
For the sake of simplicity, a geolocator imported from [Geopy](https://geopy.readthedocs.io/en/stable/) has been added for manual input, which automatically assigns coordinates to entered city names.

