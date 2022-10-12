import math


# Norden, Westen, Süden, Osten
himmelsRichtungen = ((-45, -135), (-135, -225), (-225, -315), (-315, -45))

class Pizzacut:
    def __init__(self, x, y, r, d):
        self.coordinates = (float(x), float(y))
        self.radius = float(r)
        self.direction = self.switcher_direction(d)
        self.points = self.newpoints(self.coordinates, self.radius, self.direction)


    def newpoints(self, coordinates, radius, direction):
        newpoints = ((coordinates[0] + radius * math.cos(direction[0] * math.pi/180), coordinates[1]
                      + radius * math.sin(direction[0]*math.pi / 180)),
                     (coordinates[0] + radius * math.cos(direction[1] * math.pi/180), coordinates[1]
                      + radius * math.sin(direction[1]*math.pi / 180)))
        return newpoints

    def switcher_direction(self, d):
        switcher = {
            "süd": (-225, -315),
            "süden": (-225, -315),
            "south": (-225, -315),
            "north": (-45,-135),
            "norden": (-45,-135),
            "nord": (-45,-135),
            "ost": (-315, -45),
            "osten": (-315, -45),
            "east": (-315, -45),
            "westen": (-135, -225),
            "west": (-135, -225)
        }
        return switcher.get(d, "keine Himmelsrichtung")