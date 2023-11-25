import draw
import pyclipper
from pyclipper import scale_from_clipper
from pyclipper import scale_to_clipper
from geopy.geocoders import Nominatim
import pizzacut
import csv

shapeList = list()
input_dict = {}
user_abort = False
geolocator = Nominatim(timeout=2, user_agent="Protopype")


def geocode(cityname):
    location = geolocator.geocode(cityname)
    return tuple((location.latitude, location.longitude))


def floating(textin):
    point = list(())
    i = 0
    while i < len(textin):
        if i < 2:
            point.append(float(textin[i]))
        elif i == 2:
            point.append(int(textin[i]))
        else:
            point.append(textin[i])
        i += 1
    return tuple(point)


def get_input():
    dec0 = input("(M)anually / (F)ile / File-(I)nstructions: ").lower()
    if dec0 == "f":
        csv_reader(input("Please input filepath (../file.csv): "))
    elif dec0 == "i":
        print("The CSV-file should contain the following columns: \n cs (coordinate system),"
              "coordinates, type, Index or Direction/Distance. \n The line following an object of type Between is "
              "processed as the reference object")
        get_input()
    else:
        get_input_manually()
    for z in input_dict:
        if isinstance(input_dict[z], tuple):
            if len(input_dict[z]) == 3:
                shapeList.append(pizzacut.Between((input_dict[z][0], input_dict[z][1]), width=input_dict[z][2]))
            else:
                shapeList.append(pizzacut.Between((input_dict[z][0], input_dict[z][1])))
        else:
            shapeList.append(pizzacut.Distance(input_dict[z]))


def get_input_manually():
    usercheck = False
    while not usercheck:
        zone = ""
        cs = input("Please choose your input coordinate system (u)tm/(l)atlng or type in a placename: ")
        if cs.lower() != "u" and cs.lower() != "l" and cs.lower() != "utm" and cs.lower() != "latlng":
            point = pizzacut.Place(coordinate_input=geocode(cs), cs="latlng", verweis=None, typ=None)
        else:
            coords = input("Please input your coordinates: ")
            if "u" in cs.lower():
                zone = input("please specify zone number and letter: ")
            point = pizzacut.Place(coordinate_input=floating((coords + " " + zone).split()), cs=cs,
                                   verweis=None, typ=None)
        typ = input("please name type of input: (b)etween / (d)irection: ").lower()
        if typ == "between" or typ == "b":
            point.typ = "between"
            point.verweis = 0
            zone = ""
            cs = input("Please choose your input coordinate system for second point of reference (u)tm/(l)atlng or "
                       "type in a placename: ")
            if cs.lower() != "u" and cs.lower() != "l" and cs.lower() != "utm" and cs.lower() != "latlng":
                second = pizzacut.Place(coordinate_input=geocode(cs), cs="latlng", verweis=None, typ=None)
            else:
                coords = input("Please input your coordinates: ")
                if "u" in cs.lower():
                    zone = input("please specify zone number and letter: ")
                second = pizzacut.Place(coordinate_input=floating((coords + " " + zone).split()), cs=cs, verweis=1,
                                        typ=None)
            second.typ = typ
            opt_mod = input("Relation of the two main axes (default= 0.25) ")
            if len(opt_mod) == 0:
                point = (point, second)
            else:
                point = (point, second, float(opt_mod))
        else:
            point.typ = "direction"
            point.verweis = point.set_verweis(input("Please specify Distance in Kilometers and Direction from your "
                                                    "chosen Point in Quarter or Tuple of degrees: (Distance Quarter "
                                                    "or Distance Start End): "))
        input_dict[len(input_dict)] = point
        if input("Do you want to add another Reference? (y/n) ").lower() == "n":
            usercheck = True


def csv_reader(filepath: str):
    with open(filepath) as file:
        csvreader = csv.DictReader(file)
        read_list = list()
        for row in csvreader:
            read_list.append(pizzacut.Place(cs=row["cs"], coordinate_input=floating(row["coordinates"].split()),
                                          typ=row["type"], verweis=row["verweis"]))
            print(dict(row))
        j = 0
        k = len(input_dict)
        while j < len(read_list):
            if read_list[j].typ == "between":
                input_dict[k] = (read_list[j], read_list[j + 1])
                j += 1
            else:
                input_dict[k] = read_list[j]
            j += 1
            k += 1


def csv_writer(filepath: str):
    header = ['cs', 'coordinates', 'type', 'verweis']
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        l = 0
        while l < len(input_dict):
            if isinstance(input_dict[l], tuple):
                j = 0
                while j < len(input_dict[l]):
                    coordinates = str(input_dict[l][j].utm["easting"]) + " " + str(input_dict[l][j].utm["northing"]) \
                                  + " " + str(input_dict[l][j].utm["zone_numb"]) + " " + str(input_dict[l][j].utm["zone_let"])
                    verweis = input_dict[l][j].verweis
                    row = {'cs': "utm", 'coordinates': coordinates, 'type': str(input_dict[l][j].typ), 'verweis': verweis}
                    writer.writerow(row)
                    j += 1
            else:
                coordinates = str(input_dict[l].utm["easting"]) + " " + str(input_dict[l].utm["northing"]) \
                              + " " + str(input_dict[l].utm["zone_numb"]) + " " + str(input_dict[l].utm["zone_let"])
                verweis = ' '.join(str(e) for e in input_dict[l].verweis)
                row = {'cs': "utm", 'coordinates': coordinates, 'type': str(input_dict[l].typ), 'verweis': verweis}
                writer.writerow(row)
            l += 1


def save_polygon(filepath: str, schnittflaeche):
    f = open(filepath, "w")
    f.write(str(schnittflaeche[0]) + "Zone: " + str(zone_get.utm["zone_numb"]) + str(zone_get.utm["zone_let"]))
    f.close()


def check_intersection(subj, clip):
    pc = pyclipper.Pyclipper()
    pc.AddPath(scale_to_clipper(clip), pyclipper.PT_CLIP, True)
    pc.AddPath(scale_to_clipper(subj), pyclipper.PT_SUBJECT, True)
    return scale_from_clipper(pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_POSITIVE, pyclipper.PFT_POSITIVE))


print("Start by adding your places manually or via CSV-file:")
while not user_abort:
    get_input()
    schnittflache = check_intersection(shapeList[-1].path, shapeList[0].path)
    i = 1
    while i < len(shapeList):
        schnittflache = check_intersection(shapeList[i].path, tuple(tuple(sub) for sub in schnittflache[0]))
        i += 1
    # for i in range(len(shapeList) - 1):
    #     schnittflache = check_intersection(shapeList[i - 1].path, shapeList[i].path)
    print("The clipped Polygon is modelled by: \n", schnittflache[0])
    if isinstance(input_dict[0], tuple):
        zone_get = input_dict[0][0]
    else:
        zone_get = input_dict[0]
    draw.draw(shapeList, pizzacut.latlon_conv(tuple(tuple(sub) for sub in schnittflache[0]), zone_get.utm["zone_numb"],
                                              zone_get.utm["zone_let"]))
    choice = False
    while not choice:
        restart = input("Add (n)ew Points, (s)ave input to CSV, (p)rint Clipped polygon to file or (a)bort?")
        if restart == "a":
            choice = True
            user_abort = True
        elif restart == "s":
            csv_writer(input("please input desired filename and path:(../name.csv) "))
        elif restart == "p":
            save_polygon(input("please input desired filename and path: "), schnittflache)
        else:
            choice = True
