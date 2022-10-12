# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import draw
import pizzacut

punktSammlung = list()


def getinput():
    usercheck = "y"
    print("Please add at least two points for identification")
    while usercheck == "y":
        print("Type your Coordinates")
        point = input("Format ( X Y direction distance): ").split()
        point1 = pizzacut.Pizzacut(point[0], point[1], point[3], point[2])
        punktSammlung.append(point1)
        usercheck = input("Do you want to add another point? y/n:").lower()
    if len(punktSammlung) < 2:
        punktSammlung.clear()
        print("Zu wenig Punkte")
        getinput()


# Press the green button in the gutter to run the script.
getinput()
draw.draw()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
