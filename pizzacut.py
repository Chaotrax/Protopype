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
        i += 5

    return tuple(newpoints)


class Pizzacut:
    def __init__(self, x, y, r, d):
        self.coordinates = (float(x), float(y))
        self.radius = float(r)
        self.direction = switcher_direction(d)
        self.shape = approx_arc(self.coordinates, self.radius, self.direction)

    @staticmethod
    def __print__():
        print("nüsch")


def get_angle(p1, p2):
    angle = 0
    return angle


def approx_ellipse(p1, p2):
    new_radius = math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))
    list_ell = list()
    i = 0
    while i < new_radius:
        list_ell.append(0.5 * (new_radius - 4 * math.sqrt(3 * math.pow(new_radius, 2) + 4 * new_radius * i
                                                          - 4 * math.pow(i, 2))))
        i += 1
    while i > 0:
        list_ell.append(0.5 * (new_radius + 4 * math.sqrt(3 * math.pow(new_radius, 2) + 4 * new_radius * i
                                                          - 4 * math.pow(i, 2))))
        i -= 1
    return list_ell


class Between:
    def __init__(self, p1, p2):
        self.shape = approx_ellipse(p1, p2)
