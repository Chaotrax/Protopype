import geopandas
import sympy
import utm as utm_lib
from shapely import Polygon


def latlon_conv(shapelist, zone, letter):
    newlist = []
    for i in shapelist:
        newlist.append(utm_lib.to_latlon(int(i[0]), int(i[1]), zone, letter))
    return tuple(newlist)


def switcher_direction(d):
    """
    chooses corresponding pair of degrees marking the given direction on windrose or takes a pair of degrees (tuple)

    :param d: direction in Str or tuple int
    :return: tuple int
    """
    switcher = {
        "süd": (225, 315),
        "süden": (225, 315),
        "south": (225, 315),
        "südwest": (180, 270),
        "südost": (270, 360),
        "southeast": (270, 360),
        "southwest": (180, 270),
        "north": (45, 135),
        "norden": (45, 135),
        "nord": (45, 135),
        "Nordost": (0, 90),
        "Nordwest": (90, 180),
        "Northwest": (90, 180),
        "Northeast": (0, 90),
        "ost": (315, 405),
        "osten": (315, 405),
        "east": (315, 405),
        "westen": (135, 225),
        "west": (135, 225)
    }
    if isinstance(d, str):
        return switcher.get(d.lower(), "keine Himmelsrichtung")
    return d


class DistanceObject:
    """
    Informal Interface that defines the place of an object and its shape

    ...

    Attributes
    ----------
    coordinates : tuple float
        a tuple of floats, representing the UTM-coordinates of the object

    coordinates_latlon : dict
        dictionary containing the coordinates in latitude and longitude of the object

    path : tuple float
        tuple containing the UTM-coordinates of the approximation of the generated shape

    shape : tuple float
        tuple containing coordinates of the approximation of the generated shape in Latitude and Longitude
    """

    def __init__(self, points):
        self.coordinates = points
        self.coordinates_latlon = None
        self.path = None
        self.shape = None

    def set_shape(self):
        return geopandas.GeoSeries(data=Polygon(self.path))


class Distance(DistanceObject):
    """
    Shapeobject made up of points approximating an arc with a given radius to the startingpoint

    ...

    Attributes
    __________
    direction : int
        Tuple of two ints indicating start and end degree for the geographic direction of the pizzacutshape
    radius : float
        radius of the shape in kilometers
    path : float
        tuple of utm-coordinates approximating arc
    shape : dict
        tuple containing coordinates of the approximation of the generated shape in Latitude and Longitude
    """

    def __init__(self, points):
        super().__init__(points)
        self.direction = switcher_direction(self.coordinates.verweis[1])
        self.radius = float(self.coordinates.verweis[0]) * 1000
        self.path = self.approx_arc()
        self.shape = latlon_conv(self.path, self.coordinates.utm["zone_numb"], self.coordinates.utm["zone_let"])

    def approx_arc(self):
        """
        approximates a polyline-arc for a Polygonshape given radius and direction by calculating coordinates of
        points on the arc

        :return: tuple of points (UTM-Coordinates) forming a Polygon
        """

        newpoints = [(self.coordinates.utm["easting"], self.coordinates.utm["northing"]), ]
        i = self.direction[0]
        while i <= self.direction[1]:
            easting = self.coordinates.utm["easting"] + self.radius * sympy.cos(i * sympy.pi / 180)
            northing = self.coordinates.utm["northing"] + self.radius * sympy.sin(i * sympy.pi / 180)
            newpoints.append((sympy.N(easting), sympy.N(northing)))
            i += 5
        return tuple(newpoints)


class Between(DistanceObject):
    """
    Shapeobject made up of points approximating an ellipse between two places

    ...

    Attributes
    ____________
    formel : Str
        String representing the equation that was approximated

    path : tuple
        tuple of coordinates forming the shapeobject with UTM coordinates

    shape : tuple
        tuple of coordinates forming the shapeobject with latitude and longitude coordinates
    """
    def __init__(self, points, width=0.25):
        super().__init__(points)
        self.width = width
        self.formel = None
        self.path = self.approx_ellipse(self.width)
        self.shape = latlon_conv(self.path, self.coordinates[0].utm["zone_numb"], self.coordinates[0].utm["zone_let"])

    def approx_ellipse(self, width):
        """
        Builds a polygon approximating an ellipse by using the distance between both given points
        :return: Tuple of UTM-Coordinates approximating Ellipse
        """
        new_radius = sympy.sqrt((self.coordinates[1].utm["easting"] - self.coordinates[0].utm["easting"])**2
                                + (self.coordinates[1].utm["northing"] - self.coordinates[0].utm["northing"])**2)
        angle = sympy.acos((self.coordinates[1].utm["easting"] - self.coordinates[0].utm["easting"])
                           / (sympy.sqrt((self.coordinates[1].utm["northing"] - self.coordinates[0].utm["northing"])**2
                                         + (self.coordinates[1].utm["easting"]
                                            - self.coordinates[0].utm["easting"])**2)))
        if self.coordinates[0].utm["northing"] > self.coordinates[1].utm["northing"]:
            angle = angle * -1
        list_ell = list()
        i = 0
        while i <= 360:
            x = 0.5 * new_radius * sympy.cos(i * sympy.pi / 180)
            y = width * new_radius * sympy.sin(i * sympy.pi / 180)
            easting = x * sympy.cos(angle) - y * sympy.sin(angle) + self.coordinates[0].utm["easting"]
            northing = x * sympy.sin(angle) + y * sympy.cos(angle) + self.coordinates[0].utm["northing"]
            if i == 0:
                x_origin = easting
                y_origin = northing
            if angle > 0:
                if angle > sympy.pi/2:
                    easting = easting - abs(self.coordinates[0].utm["easting"] - x_origin)
                    northing = northing + abs(self.coordinates[0].utm["northing"] - y_origin)
                else:
                    easting = easting + abs(self.coordinates[0].utm["easting"] - x_origin)
                    northing = northing + abs(self.coordinates[0].utm["northing"] - y_origin)
            else:
                if -angle < sympy.pi/2:
                    easting = easting + abs(self.coordinates[0].utm["easting"] - x_origin)
                    northing = northing - abs(self.coordinates[0].utm["northing"] - y_origin)
                else:
                    easting = easting - abs(self.coordinates[0].utm["easting"] - x_origin)
                    northing = northing - abs(self.coordinates[0].utm["northing"] - y_origin)
            list_ell.append((sympy.N(easting),
                             sympy.N(northing)))
            i += 10
        return tuple(list_ell)


class Place:
    """
    Object representing a place on a map

    ...

    Attributes
    __________
    name : Str
        name of the place

    input_coordsystem : Str
        coordinate-system used while initializing the object

    utm : dict
        dictionary containing utm coordinates, zone number and zone letter

    latlng: dict
        dictionary containing latitude and longitude
    """

    def __init__(self, coordinate_input: tuple, cs: str, typ, verweis):
        self.typ = typ
        self.verweis = self.set_verweis(verweis)
        self.input_coordsystem = self.check_coordsystem(cs.lower())
        self.utm = self.process_utm(coordinate_input)
        self.latlng = self.process_latlng(coordinate_input)

    def check_coordsystem(self, cs):
        if (cs == "u") or (cs == "utm"):
            return "utm"
        else:
            return "latlng"

    def set_verweis(self, verweis_check):
        if self.typ == "between":
            return int(verweis_check)
        elif self.typ is None:
            return verweis_check
        else:
            return verweis_check.split()

    def process_utm(self, coordinate_input):
        """
        Process input-coordinates into dict

        :param coordinate_input: tuple coordinates as floats used as parameter when initializing object
        :return: dictionary containing UTM coordinates, zone number and zone letter
        """

        if self.input_coordsystem == "utm":
            return {"easting": coordinate_input[0], "northing": coordinate_input[1], "zone_numb": coordinate_input[2],
                    "zone_let": coordinate_input[3]}
        else:
            conv = utm_lib.from_latlon(coordinate_input[0], coordinate_input[1])
            return {"easting": conv[0], "northing": conv[1], "zone_numb": conv[2], "zone_let": conv[3]}

    def process_latlng(self, coordinate_input):
        """
        Process input-coordinates into dict

        :param coordinate_input: tuple coordinates as floats used as parameter when initializing object
        :return: dictionary containing coordinates in latitude and longitude
        """
        if self.input_coordsystem == "latlng":
            return {"latitude": coordinate_input[0], "longitude": coordinate_input[1]}
        else:
            conv = utm_lib.to_latlon(coordinate_input[0], coordinate_input[1], coordinate_input[2], coordinate_input[3])
            return {"latitude": conv[0], "longitude": conv[1]}
