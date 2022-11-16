import sympy


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
    # newpoints = ((coordinates[0] + radius * sympy.cos(direction[0] * sympy.pi/180), coordinates[1]
    #               + radius * sympy.sin(direction[0]*sympy.pi / 180)),
    #              (coordinates[0] + radius * sympy.cos(direction[1] * sympy.pi/180), coordinates[1]
    #               + radius * sympy.sin(direction[1]*sympy.pi / 180)))
    newpoints = [coordinates]
    i = direction[0]
    while i <= direction[1]:
        newpoints.append((coordinates[0] + radius * sympy.cos(i * sympy.pi / 180), coordinates[1] + radius
                          * sympy.sin(i * sympy.pi / 180)))
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


def rot_ell(sh_ell, angle):
    newsh_ell = list()
    for i in sh_ell:
        newsh_ell.append((i[0] * sympy.cos(angle) - i[1] * sympy.sin(angle), i[0] * sympy.sin(angle) + i[1]
                          * sympy.cos(angle)))
    return newsh_ell


def approx_ellipse(pt1, pt2):
    new_radius = sympy.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
    angle = (360 - sympy.asin((pt1[1] - pt2[1]) / new_radius)) * sympy.pi / 180
    list_ell = list()
    i = 0
    while i < new_radius:
        list_ell.append((pt1[0] + i, 0.5 * (new_radius - 4 * sympy.sqrt(3 * new_radius**2 + 4 * new_radius * i
                                                                        - 4 * i**2))))
        i += 1
    while i > 0:
        list_ell.append((pt1[0] + i, 0.5 * (new_radius + 4 * sympy.sqrt(3 * new_radius**2 + 4 * new_radius * i
                                                                        - 4 * i**2))))
        i -= 1

    return rot_ell(list_ell, angle)


class Between:
    def __init__(self, p1, p2):
        self.shape = approx_ellipse(p1, p2)
