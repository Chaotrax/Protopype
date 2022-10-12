# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import circleMath
import pizzacut


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def getinput():
    print("Type your Coordinates")
    point = input("Format ( X Y direction distance): ").split()
    point1 = pizzacut.Pizzacut(point[0], point[1], point[3], point[2])
    print(point1.coordinates, point1.radius, point1.direction)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    getinput()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
