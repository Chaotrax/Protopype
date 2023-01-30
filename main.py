# Press Umschalt+F10 to execute it or replace it with your code.

import draw
import pyclipper
from pyclipper import scale_from_clipper
from pyclipper import scale_to_clipper
import pizzacut

shapeList = list()


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
    return point


def get_input():
    usercheck = "y"
    print("Please add at least two Shapes for identification ")
    while usercheck == "y":
        # model first point as Place
        point = list((pizzacut.Place(
            floating(input("Please add your coordinates in latlng or UTM (X Y ((Number) (Letter))): ").split()),
            "Startpunkt"),))
        if input("Distance or Between? (d/b): ") == "b":
            # model second point as place and append to point which is passed to Between
            point.append(
                pizzacut.Place(floating(input("Please add the second Point (X Y ((Number) (Letter))): ").split()),
                               "Second Point"))
            shapeList.append(pizzacut.Between(tuple(point)))
            print(shapeList[-1].path)
        else:
            for i in input("Please specify Distance in Kilometers"
                           " and Direction from your chosen Point: (Distance Quarter)").split():
                point.append(i)
            shapeList.append(pizzacut.Distance(point[0], float(point[1]), point[2]))
        usercheck = input("Do you want to add another Shape? y/n: ")
    if len(shapeList) < 2:
        shapeList.clear()
        print("Zu wenig Punkte!")
        get_input()


def check_intersection(subj, clip):
    # POLYGONE aufstellen -> näherungsweise bestimmen über Segmente. (wieviele Segmente ist sinnvol? teil von
    # pizzacut.py als funktion.
    # xor nutzen für fuzzy angaben (schwankende angaben)
    pc = pyclipper.Pyclipper()
    pc.AddPath(scale_to_clipper(clip), pyclipper.PT_CLIP, True)
    pc.AddPath(scale_to_clipper(subj), pyclipper.PT_SUBJECT, True)
    print("test")
    return scale_from_clipper(pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_POSITIVE, pyclipper.PFT_POSITIVE))


get_input()
schnittflache = check_intersection(shapeList[-1].path, shapeList[0].path)
# for i in range(len(shapeList) - 1):
#     schnittflache = check_intersection(shapeList[i-1].shape, shapeList[i].shape)
print(schnittflache)
draw.draw(shapeList)
# geolist = list()
# for i in shapeList:
#     geolist.append(i.shape)
# pizzacut.create_gdf(tuple(geolist))
# draw.draw(schnittflache)  # TODO

# Was passiert wenn zwei angaben übereinstimmen aber die dritte nicht?
# TODO
# Koordinatenübertragung in UTM für Berechnungen. Umwandlung in UTM
# zurück in Latlng für ausgabe
