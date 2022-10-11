# Berechnungen
import math

# Norden, Westen, Süden, Osten
himmelsRichtungen = ((-45, -135), (-135, -225), (-225, -315), (-315, -45))


def kreisbogen(coords):
    for x in coords:
        points = tuple(x.split())
        arcpoints(points)


def arcpoints(points):
    print(points)

