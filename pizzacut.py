import geopandas
import sympy
import utm as utm_lib
from shapely import Polygon


# def create_gdf(geolist: tuple):
#     gs = geolist[0]
#     for i in range(len(geolist)):
#         gs.append(geolist[i + 1])
#     geopandas.GeoDataFrame(geometry=gs).plot()

def latlon_conv(shapelist, zone, letter):
    newlist = []
    for i in shapelist:
        newlist.append(utm_lib.to_latlon(i[0], i[1], zone, letter))
    return tuple(newlist)


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
    def __init__(self, points):
        self.coordinates = points
        self.coordinates_latlon = None
        self.path = None
        self.shape = None

    def set_shape(self):
        return geopandas.GeoSeries(data=Polygon(self.path))


class Distance(DistanceObject):
    def __init__(self, points, radius: float, direction):
        super().__init__(points)
        self.direction = switcher_direction(direction)
        self.radius = radius * 1000
        self.path = self.approx_arc()
        self.shape = latlon_conv(self.path, self.coordinates.utm["zone_numb"], self.coordinates.utm["zone_let"])

    def approx_arc(self):
        newpoints = [(self.coordinates.utm["easting"], self.coordinates.utm["northing"]), ]
        i = self.direction[0]
        while i <= self.direction[1]:
            easting = self.coordinates.utm["easting"] + self.radius * sympy.cos(i * sympy.pi / 180)
            northing = self.coordinates.utm["northing"] + self.radius * sympy.sin(i * sympy.pi / 180)
            newpoints.append((easting, northing))
            i += 5
        return tuple(newpoints)


class Between(DistanceObject):
    def __init__(self, points):
        super().__init__(points)
        self.formel = None
        self.path = self.approx_ellipse()
        self.shape = latlon_conv(self.path, self.coordinates[0].utm["zone_numb"], self.coordinates[0].utm["zone_let"])

    def approx_ellipse(self):
        new_radius = sympy.sqrt((self.coordinates[1].utm["easting"] - self.coordinates[0].utm["easting"]) ** 2 + (self.coordinates[1].utm["northing"] - self.coordinates[0].utm["northing"]) ** 2)
        angle = (360 - sympy.asin((self.coordinates[0].utm["northing"] - self.coordinates[1].utm["northing"]) / new_radius)) * sympy.pi / 180
        print("neue variablen erechnet")
        list_ell = list()
        list_ell.append((self.coordinates[0].utm["easting"], self.coordinates[0].utm["northing"]))
        # schleife bearbeiten
        i = 0
        while i < new_radius:
            list_ell.append((self.coordinates[0].utm["easting"] + i, 0.5 * (new_radius - 4 * sympy.sqrt(3 * new_radius ** 2 + 4 * new_radius * i - 4 * i ** 2))))
            i += new_radius / 10
        list_ell.append((self.coordinates[1].utm["easting"], self.coordinates[1].utm["northing"]))
        print("erster Bogen")
        while i > 0:
            list_ell.append((self.coordinates[0].utm["easting"] + i, 0.5 * (new_radius + 4 * sympy.sqrt(3 * new_radius ** 2 + 4 * new_radius * i - 4 * i ** 2))))
            i -= new_radius / 10
        list_ell = list(dict.fromkeys(list_ell))
        print("zweiter Bogen")
        return self.rot_ell(list_ell, angle)

    def rot_ell(self, sh_ell, angle):
        newsh_ell = list()
        for i in sh_ell:
            newsh_ell.append((i[0] * sympy.cos(angle) - i[1] * sympy.sin(angle), i[0] * sympy.sin(angle) + i[1]
                              * sympy.cos(angle)))
        return tuple(newsh_ell)


class Place:
    def __init__(self, coordinate_input, name):
        self.name = name
        self.input_coordsystem = self.check_coordsystem(coordinate_input)
        self.utm = self.process_utm(coordinate_input)
        self.latlng = self.process_latlng(coordinate_input)

    def check_coordsystem(self, coordinate_input):
        if len(coordinate_input) > 2:
            return "utm"
        else:
            return "latlng"

    def process_utm(self, coordinate_input):
        if self.input_coordsystem == "utm":
            return {"easting": coordinate_input[0], "northing": coordinate_input[1], "zone_numb": coordinate_input[2],
                    "zone_let": coordinate_input[3]}
        else:
            conv = utm_lib.from_latlon(coordinate_input[0], coordinate_input[1])
            return {"easting": conv[0], "northing": conv[1], "zone_numb": conv[2], "zone_let": conv[3]}

    def process_latlng(self, coordinate_input):
        if self.input_coordsystem == "latlng":
            return {"latitude": coordinate_input[0], "longitude": coordinate_input[1]}
        else:
            conv = utm_lib.to_latlon(coordinate_input[0], coordinate_input[1], coordinate_input[2], coordinate_input[3])
            return {"latitude": conv[0], "longitude": conv[1]}

# TODO: use place instead of tuples
