import sympy

#
# def approx_arc(coordinates, radius, direction):
#     # newpoints = ((coordinates[0] + radius * sympy.cos(direction[0] * sympy.pi/180), coordinates[1]
#     #               + radius * sympy.sin(direction[0]*sympy.pi / 180)),
#     #              (coordinates[0] + radius * sympy.cos(direction[1] * sympy.pi/180), coordinates[1]
#     #               + radius * sympy.sin(direction[1]*sympy.pi / 180)))
#     newpoints = [coordinates]
#     i = direction[0]
#     while i <= direction[1]:
#         newpoints.append((coordinates[0] + radius * sympy.cos(i * sympy.pi / 180), coordinates[1] + radius
#                           * sympy.sin(i * sympy.pi / 180)))
#         i += 5
#
#     return tuple(newpoints)


# class Pizzacut:
#     def __init__(self, x, y, r, d):
#         self.coordinates = (float(x), float(y))
#         self.radius = float(r)
#         self.direction = switcher_direction(d)
#         self.shape = approx_arc(self.coordinates, self.radius, self.direction)
#
#     @staticmethod
#     def __print__():
#         print("nüsch")


# def rot_ell(sh_ell, angle):
#     newsh_ell = list()
#     for i in sh_ell:
#         newsh_ell.append((i[0] * sympy.cos(angle) - i[1] * sympy.sin(angle), i[0] * sympy.sin(angle) + i[1]
#                           * sympy.cos(angle)))
#     return newsh_ell


# def approx_ellipse(pt1, pt2):
#     new_radius = sympy.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)
#     angle = (360 - sympy.asin((pt1[1] - pt2[1]) / new_radius)) * sympy.pi / 180
#     list_ell = [pt1]
#     # schleife bearbeiten
#     i = 0
#     while i < new_radius:
#         list_ell.append((pt1[0] + i, 0.5 * (new_radius - 4 * sympy.sqrt(3 * new_radius ** 2 + 4 * new_radius * i
#                                                                         - 4 * i ** 2))))
#         i += 1
#     list_ell.append(pt2)
#     while i > 0:
#         list_ell.append((pt1[0] + i, 0.5 * (new_radius + 4 * sympy.sqrt(3 * new_radius ** 2 + 4 * new_radius * i
#                                                                         - 4 * i ** 2))))
#         i -= 1
#     list_ell = list(dict.fromkeys(list_ell))
#     return rot_ell(list_ell, angle)


# class Between:
#     def __init__(self, p1, p2):
#         self.c1 = (float(p1[0]), float(p1[1]))
#         self.c2 = (float(p2[0]), float(p2[1]))
#         self.shape = approx_ellipse(self.c1, self.c2)

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


class DistanceObject:
    def __init__(self, points: tuple):
        self.coordinates = points
        self.path = None
        self.shape = None


class Distance(DistanceObject):
    def __init__(self, points: tuple, radius: float, direction):
        super().__init__(points)
        self.path = self.approx_arc()
        self.radius = radius
        self.direction = switcher_direction(direction)

    def approx_arc(self):
        newpoints = [self.coordinates]
        i = self.direction[0]
        while i <= self.direction[1]:
            newpoints.append((self.coordinates[0] + self.radius * sympy.cos(i * sympy.pi / 180), self.coordinates[1]
                              + self.radius * sympy.sin(i * sympy.pi / 180)))
            i += 5
        return tuple(newpoints)


class Between(DistanceObject):
    def __init__(self, points: tuple):
        super().__init__(points)
        self.path = self.approx_ellipse()

    def approx_ellipse(self):
        new_radius = sympy.sqrt((self.coordinates[1][0] - self.coordinates[0][0]) ** 2 + (self.coordinates[1][1]
                                - self.coordinates[0][1]) ** 2)
        angle = (360 - sympy.asin((self.coordinates[0][1] - self.coordinates[1][1]) / new_radius)) * sympy.pi / 180
        list_ell = [self.coordinates[0]]
        # schleife bearbeiten
        i = 0
        while i < new_radius:
            list_ell.append((self.coordinates[0][0] + i, 0.5 * (new_radius - 4 * sympy.sqrt(3 * new_radius ** 2 + 4
                            * new_radius * i - 4 * i ** 2))))
            i += 1
        list_ell.append(list(self.coordinates[1]))
        while i > 0:
            list_ell.append((self.coordinates[0][0] + i, 0.5 * (new_radius + 4 * sympy.sqrt(3 * new_radius ** 2 + 4
                            * new_radius * i - 4 * i ** 2))))
            i -= 1
        list_ell = list(dict.fromkeys(list_ell))
        return self.rot_ell(list_ell, angle)

    def rot_ell(self, sh_ell, angle):
        newsh_ell = list()
        for i in sh_ell:
            newsh_ell.append((i[0] * sympy.cos(angle) - i[1] * sympy.sin(angle), i[0] * sympy.sin(angle) + i[1]
                              * sympy.cos(angle)))
        return newsh_ell
