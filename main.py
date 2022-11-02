# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import draw
import pyclipper
from pyclipper import scale_from_clipper
from pyclipper import scale_to_clipper
import pizzacut

punktSammlung = list()


def get_input():
    usercheck = "y"
    print("Please add at least two points for identification")
    while usercheck == "y":
        print("Type your Coordinates")
        point = clean_input(input("Format ( X Y direction distance): ").split())
        punktSammlung.append(pizzacut.Pizzacut(point[0], point[1], point[3], point[2]))
        usercheck = input("Do you want to add another point? y/n:").lower()
    if len(punktSammlung) < 2:
        punktSammlung.clear()
        print("Zu wenig Punkte")
        get_input()
    for j in punktSammlung:
        print(j.coordinates, j.shape)


def clean_input(raw_input):
    cleaned_input = raw_input
    return cleaned_input


def check_intersection(subj, clip):
    # POLYGONE aufstellen -> näherungsweise bestimmen über Segmente. (wieviele Segmente ist sinnvol? teil von
    # pizzacut.py als funktion.
    # xor nutzen für fuzzy angaben (schwankende angaben)
    pc = pyclipper.Pyclipper()
    pc.AddPath(scale_to_clipper(clip), pyclipper.PT_CLIP, True)
    pc.AddPath(scale_to_clipper(subj), pyclipper.PT_SUBJECT, True)
    return scale_from_clipper(pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_POSITIVE, pyclipper.PFT_POSITIVE))


# Press the green button in the gutter to run the script.
get_input()
for i in range(len(punktSammlung) - 1):
    print("Schnittfläche: " + check_intersection(punktSammlung[i].shape, punktSammlung[i + 1].shape))
draw.draw()  # TODO

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# Was passiert wenn zwei angaben übereinstimmen aber die dritte nicht?
