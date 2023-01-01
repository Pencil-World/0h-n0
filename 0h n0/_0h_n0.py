import pyautogui
import numpy as np
from PIL import Image
from Cell import Cell
import keyboard
import time

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

width = 25
shifts = [] #advanced pixel comparisons
reds = []
blues = []
coord = [0, -1]
screen = Image.open('screen.png')
keyboard.wait('ENTER')

# screen = pyautogui.screenshot('screen.png', region = (470, 475))
# pyautogui.screenshot('The One.png', region = (942 - width / 2, 539 - width / 2, width, width))
board = [[10, 10, 10, 10, 10, 6, 9, -1, 10], 
         [5, 10, 10, 6, 10, 10, 10, 3, 10], 
         [5, 10, 10, 10, -1, 10, 10, 10, 10], 
         [-1, 10, 10, 7, 10, 10, 10, 10, 10], 
         [4, 10, -1, 10, 2, 10, 10, 10, 5], 
         [10, -1, 3, 10, 10, 5, 10, 10, -1], 
         [10, 10, 4, 10, -1, 10, 2, 10, 10], 
         [10, 7, 10, 10, 10, 6, 10, 5, 10], 
         [10, 3, 10, 10, 10, 5, 10, 10, 5]]

for y in range(0, 9):
    for x in range(0, 9):
        val = board[y][x]
        if val == 10:
            Cell.board[y][x] = Cell(x, y)
        else:
            Cell.board[y][x] = Cell(x, y, None if board[y][x] == 10 else board[y][x])
            if val > 0:
                blues.append(Cell.board[itY][itX])

#for width in range(8, -1, -1):
#    for it in range(1, -1, -1):
#        for temp in range(width + it):
#            coord[it] += -1 if width % 2 else 1
#            itX, itY = coord[1], coord[0]
#            if board[itX][itY] == 10:
#                Cell.board[itY][itX] = Cell(itX, itY)
#            else:
#                Cell.board[itY][itX] = Cell(itX, itY, board[itX][itY])
#                if board[itX][itY] == -1:
#                    reds.append(Cell.board[itY][itX])
#                else:
#                    blues.append(Cell.board[itY][itX])
#            Cell.board[itY][itX].init() # remove?

#for width in range(8, -1, -1):
#    for it in range(1, -1, -1):
#        for temp in range(width + it):
#            coord[it] += -1 if width % 2 else 1
#            itX, itY = coord[1], coord[0]
#            pixel = screen.getpixel((X[itX], Y[itY]))

#            if pixel == (238, 238, 238):
#                Cell.board[itY][itX] = Cell(itX, itY)
#            elif pixel == (255, 56, 75):
#                Cell.board[itY][itX] = Cell(itX, itY, -1)
#                reds.append(Cell.board[itY][itX])
#            else:
#                for number in range(1, 10):
#                    if pyautogui.locate(str(number) + '.png', screen, region = (X[itX] - width // 2, Y[itY] - width // 2, width, width), confidence = 0.85):
#                        Cell.board[itY][itX] = Cell(itX, itY, number)
#                        blues.append(Cell.board[itY][itX])
#print([item.state for item in Cell.board[:,x]])
#print([item.state for item in Cell.board[y:9,x]])

print(Cell.board)
for cell in reds:
    cell.initRed()
for cell in blues:
    cell.initBlue()
    cell.init()

for cell in blues:
    cell.predict()
print(Cell.board)
#pyautogui.click(100, 200)
#pyautogui.doubleClick(100, 200)
time.sleep(5)