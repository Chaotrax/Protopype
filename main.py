# Press Umschalt+F10 to execute it or replace it with your code.
# import geopandas

import draw
import pyclipper
from pyclipper import scale_from_clipper
from pyclipper import scale_to_clipper
import pizzacut
import csv

shapeList = list()
input_dict = {}
user_abort = False


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
    # check if user wants to input file or manually
    # when using file : csv or geojson?
    # when manually : latlng, utm or geocoding
    dec0 = input("(M)anually / (F)ile / File-(I)nstructions: ").lower()
    if dec0 == "f":
        csv_reader(input("Please input filepath (../file.csv): "))
    elif dec0 == "i":
        print("The CSV-file should contain the following columns: \n cs (coordinate system),"
              " coordinates, type, Index or Direction/Distance")
        get_input()
    else:
        get_input_manually()
    marked_indices = []
    for z in input_dict:
        if input_dict[z].typ == "between":
            if z not in marked_indices:
                shapeList.append(pizzacut.Between((input_dict[z], input_dict[int(input_dict[z].verweis)])))
                marked_indices.append(int(input_dict[z].verweis))
        else:
            shapeList.append(pizzacut.Distance(input_dict[z]))


def get_input_manually():
    k_start = len(input_dict)
    usercheck = False
    while not usercheck:
        zone = ""
        cs = input("Please choose your input coordinate system (u)tm/(l)atlng: ")
        coords = input("Please input your coordinates: ")
        if cs.lower() == "u":
            zone = input("please specify zone number and letter: ")
        point = pizzacut.Place(coordinate_input=floating((coords + " " + zone).split()), cs=cs, verweis=None, typ=None)
        input_dict[len(input_dict)] = point
        if input("Do you want to add another Place? (y/n) ").lower() == "n":
            usercheck = True
    # print all points after input
    print("please add the intended method of computing: ")
    k = 0
    # TODO test ob Fehler mit Zählung
    while k < (len(input_dict)-k_start):
        typ = input("please add type of input: between / direction: ").lower()
        if typ == "between":
            input_dict[k].typ = typ
            input_dict[k].verweis = input("Please name index of second point: ")
        else:
            input_dict[k].typ = typ
            input_dict[k].verweis = input("Please specify Distance in Kilometers"
                                          "and Direction from your chosen Point in Quarter or Tuple of degrees: ("
                                          "Distance Quarter/)")
        k += 1


def csv_reader(filepath: str):
    with open(filepath) as file:
        csvreader = csv.DictReader(file)
        j = len(input_dict)
        for row in csvreader:
            input_dict[j] = pizzacut.Place(cs=row["cs"], coordinate_input=floating(row["coordinates"].split()),
                                           typ=row["type"], verweis=row["verweis"])
            print(dict(row))
            j += 1


def csv_writer(filepath: str):
    header = ['cs', 'coordinates', 'type', 'verweis']
    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for i in input_dict:
            coordinates = str(input_dict[i].utm["easting"]) + " " + str(input_dict[i].utm["northing"]) \
                          + " " + str(input_dict[i].utm["zone_numb"]) + " " + str(input_dict[i].utm["zone_let"])
            if input_dict[i].typ == "between":
                verweis = input_dict[i].verweis
            else:
                verweis = ' '.join(str(e) for e in input_dict[i].verweis)
            row = {'cs': "utm", 'coordinates': coordinates, 'type': str(input_dict[i].typ), 'verweis': verweis}
            writer.writerow(row)


def save_polygon(filepath: str, schnittflache):
    f = open(filepath, "w")
    f.write(str(schnittflache))
    f.close()


def check_intersection(subj, clip):
    # POLYGONE aufstellen -> näherungsweise bestimmen über Segmente. (wieviele Segmente ist sinnvol? teil von
    # pizzacut.py als funktion.
    # xor nutzen für fuzzy angaben (schwankende angaben)
    pc = pyclipper.Pyclipper()
    pc.AddPath(scale_to_clipper(clip), pyclipper.PT_CLIP, True)
    pc.AddPath(scale_to_clipper(subj), pyclipper.PT_SUBJECT, True)
    return scale_from_clipper(pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_POSITIVE, pyclipper.PFT_POSITIVE))


print("Start by adding your places manually or via CSV-file:")
while not user_abort:
    get_input()
    schnittflache = check_intersection(shapeList[-1].path, shapeList[0].path)
    for i in range(len(shapeList) - 1):
        schnittflache = check_intersection(shapeList[i-1].path, shapeList[i].path)
    print("The clipped Polygon is modelled by: \n", schnittflache)
    draw.draw(shapeList)
    choice = False
    while not choice:
        restart = input("Add (n)ew Points, (s)ave input to CSV, (p)rint Clipped polygon to file or (a)bort?")
        if restart == "a":
            choice = True
            user_abort = True
        elif restart == "s":
            csv_writer(input("please input desired filename and path: "))
        elif restart == "p":
            save_polygon(input("please input desired filename and path: "), schnittflache)
        else:
            choice = True

# TODO
# https://geopandas.org/en/stable/docs/user_guide/geocoding.html#geocoding
