# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import draw
import pyclipper
import pizzacut

punktSammlung = list()


def get_input():
    usercheck = "y"
    print("Please add at least two points for identification")
    while usercheck == "y":
        print("Type your Coordinates")
        point = input("Format ( X Y direction distance): ").split()
        punktSammlung.append(pizzacut.Pizzacut(point[0], point[1], point[3], point[2]))
        usercheck = input("Do you want to add another point? y/n:").lower()
    if len(punktSammlung) < 2:
        punktSammlung.clear()
        print("Zu wenig Punkte")
        get_input()
    for i in punktSammlung:
        print(i.coordinates)


#  TODO
def check_intersection():
    # POLYGONE aufstellen -> näherungsweise bestimmen über Segmente. (wieviele Segmente ist sinnvol? teil von
    # pizzacut.py als funktion.
    # xor nutzen für fuzzy angaben (schwankende angaben)

    print("placeholder")


# Press the green button in the gutter to run the script.
get_input()
draw.draw()  # TODO

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
