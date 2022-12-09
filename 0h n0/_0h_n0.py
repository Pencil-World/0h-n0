import pyautogui
import numpy as np
from PIL import Image
from Cell import Cell

#print("Press 'ENTER' to start the program")
#input()

X = []
Y = []
board = np.zeros([9, 9])

for index in range(9):
    X.append(58.75 * index + 705)
    Y.append(59.375 * index + 300)

girth = 25
screen = Image.open('screen.png')
# screen = pyautogui.screenshot('screen.png')
# pyautogui.screenshot('The One.png', region = (942 - girth / 2, 539 - girth / 2, girth, girth))
for itY in range(9):
    for itX in range(9):
        pixel = screen.getpixel((X[itX], Y[itY]))
        if pixel == (238, 238, 238):
            continue
        elif pixel == (255, 56, 75):
            continue
        for number in range(1, 10):
            if pyautogui.locate(str(number) + '.png', 'screen.png', region = (int(X[itX] - girth / 2), int(Y[itY] - girth / 2), girth, girth), confidence = 0.85):
                board[itY][itX] = number
print(board)
#pyautogui.click(100, 200)
#pyautogui.doubleClick(100, 200)