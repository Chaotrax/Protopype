# Press Umschalt+F10 to execute it or replace it with your code.

import draw
import pyclipper
from pyclipper import scale_from_clipper
from pyclipper import scale_to_clipper
import pizzacut


shapeList = list()


# def get_input():
#     usercheck = "y"
#     print("Please add at least two points for identification")
#     while usercheck == "y":
#         decision = input("Please choose between distance and between. d / b: ")
#         if decision == "b":
#             point1 = input("Please add Point 1: X Y").split()
#             point2 = input("Please add Point 2: X Y").split()
#             punktSammlung.append(pizzacut.Between(point1, point2))
#         elif decision == "d":
#             print("Type your Coordinates")
#             point = input("Format ( X Y direction distance): ").split()
#             punktSammlung.append(pizzacut.Pizzacut(point[0], point[1], point[3], point[2]))
#         usercheck = input("Do you want to add another Variable? y/n:").lower()
#     if len(punktSammlung) < 2:
#         punktSammlung.clear()
#         print("Zu wenig Punkte")
#         get_input()
#     for j in punktSammlung:
#         print(j.coordinates, j.shape)


def splitnfloat(textin, typ):
    if typ == "e":
        return pizzacut.Between(((float(textin[0]), float(textin[1])), (float(textin[2]), float(textin[3]))))
    else:
        return pizzacut.Distance((float(textin[0]), float(textin[1])), float(textin[2]), textin[3])


def get_input():
    usercheck = "y"
    print("Please add at least two Shapes for identification ")
    while usercheck == "y":
        point = input("Please add your coordinates (X Y): ").split()
        if input("Distance or Between? (d/b): ") == "b":
            for i in input("Please add the second Point (X Y): ").split():
                point.append(i)
            shapeList.append(splitnfloat(point, "e"))
            print(shapeList[-1].path)
        else:
            for i in input("Please specify Distance and Direction from your chosen Point: (Distance Quarter)").split():
                point.append(i)
            shapeList.append(splitnfloat(point, "d"))
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
schnittflache = check_intersection(shapeList[-1].shape, shapeList[0].shape)
# for i in range(len(shapeList) - 1):
#     schnittflache = check_intersection(shapeList[i-1].shape, shapeList[i].shape)
print(schnittflache)
draw.draw(schnittflache)  # TODO

# Was passiert wenn zwei angaben übereinstimmen aber die dritte nicht?
