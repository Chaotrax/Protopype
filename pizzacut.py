import math


# Norden, Westen, Süden, Ostens
def switcher_direction(d):
    switcher = {
        "süd": (225, 315),
        "süden": (225, 315),
        "south": (225, 315),
        "north": (45, 135),
        "norden": (45, 135),
        "nord": (45, 135),
        "ost": (315, 405),
        "osten": (315, 405),
        "east": (315, 405),
        "westen": (135, 225),
        "west": (135, 225)
    }
    return switcher.get(d.lower(), "keine Himmelsrichtung")


def approx_arc(coordinates, radius, direction):
    # newpoints = ((coordinates[0] + radius * math.cos(direction[0] * math.pi/180), coordinates[1]
    #               + radius * math.sin(direction[0]*math.pi / 180)),
    #              (coordinates[0] + radius * math.cos(direction[1] * math.pi/180), coordinates[1]
    #               + radius * math.sin(direction[1]*math.pi / 180)))
    newpoints = [coordinates]
    i = direction[0]
    while i <= direction[1]:
        newpoints.append((coordinates[0] + radius * math.cos(i * math.pi / 180), coordinates[1] + radius
                          * math.sin(i * math.pi / 180)))
        i += 10

    return tuple(newpoints)


class Pizzacut:
    def __init__(self, x, y, r, d):
        self.coordinates = (float(x), float(y))
        self.radius = float(r)
        self.direction = switcher_direction(d)
        self.shape = approx_arc(self.coordinates, self.radius, self.direction)
