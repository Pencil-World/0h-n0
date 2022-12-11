import pyautogui
import numpy as np
from PIL import Image
from Cell import Cell

"""
Cell [0, 0] dimensions
    Left value: 678
    Right value: 731
    Top value: 275
    Bottom value: 328
    Diameter: 53
Cell [8, 8] dimensions
    Left value: 1151
    Right value: 1204
    Top value: 749
    Bottom value: 802
    Diameter: 53
Together
    [941, 538.5]
    [941, 538]
    # <= 0.5: round down
    # > 0.5: round up
    X: (1204 - 731) / 8 = (1151 - 678) / 8 = 59.125
    Y: (802 - 328) / 8 = (749 - 275) / 8 = 59.25
"""

#print("Press 'ENTER' to start the program")
#input()

X = []
Y = []
for index in range(9):
    X.append(round(59.125 * index + 704.4))
    Y.append(round(59.25 * index + 301.4))

length = 25
shifts = []
left = X[0] - length / 2
top = Y[0] - length / 2
screen = Image.open('screen.png')
# screen = pyautogui.screenshot('screen.png', region = (470, 475))
# pyautogui.screenshot('The One.png', region = (942 - length / 2, 539 - length / 2, length, length))
#board = np.full([9, 9], None, Cell)

reds = []
blues = []
for itY in range(9):
    for itX in range(9):
        pixel = screen.getpixel((X[itX], Y[itY]))
        if pixel == (238, 238, 238):
            Cell.board[itY][itX] = Cell(itX, itY)
            continue
        elif pixel == (255, 56, 75):
            Cell.board[itY][itX] = Cell(itX, itY, -1)
            reds.append(Cell.board[itY][itX])
            continue
        for number in range(1, 10):
            if pyautogui.locate(str(number) + '.png', screen, region = (int(X[itX] - length / 2), int(Y[itY] - length / 2), length, length), confidence = 0.85):
                Cell.board[itY][itX] = Cell(itX, itY, number)
                blues.append(Cell.board[itY][itX])

x = 1
y = 2
Cell.print()

print([item.state for item in Cell.board[:,x]])
print([item.state for item in Cell.board[y:9,x]])
for cell in reds:
    cell.initRed()
for cell in blues:
    cell.initBlue()

for cell in blues:
    cell.predict()
Cell.print()
#pyautogui.click(100, 200)
#pyautogui.doubleClick(100, 200)