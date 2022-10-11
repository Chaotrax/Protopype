# This is a sample Python script.
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import circleMath


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def getinput():
    print("Type your Coordinates")
    point = list()
    i = 0
    while i < 3:
        i += 1
        point.append(input("Format ( X Y direction distance): "))
    circleMath.kreisbogen(point)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    getinput()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
