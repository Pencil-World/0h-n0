from Cell import Cell
from PIL import Image
import keyboard
import numpy as np
import pyautogui as gui
import sys
import time

def CreateGrid():
    print("CreateGrid")
    for index in range(9):
        X.append(round(59.125 * index + 0.4))
        Y.append(round(59.25 * index + 0.4))
    
    # print(X)
    # print(Y)

def ImportBoard():
    print("ImportBoard")
    board = [[0, 4, 0, 0, 0, 0, 0, 0, 4], 
             [0, 4, 0,-1, 0, 0, 8, 0,-1], 
             [3, 0, 0, 0, 3, 0, 0, 0, 2], 
             [0, 0, 1, 0, 0, 0, 6, 0, 0], 
             [0, 0, 0, 0, 4, 0, 0, 4, 2], 
             [0, 5, 0, 3, 0, 0, 0, 3, 0], 
             [0, 0, 5, 0,-1, 2, 0, 0, 0], 
             [4, 0, 0, 0, 0, 0, 3, 0, 2], 
             [0, 9, 0, 0, 0, 0, 0, 0, 0]]
    #board = [[0, 0, 0, 0, 0, 6, 9, -1,0], 
    #         [5, 0, 0, 6, 0, 0, 0, 3, 0], 
    #         [5, 0, 0, 0, -1,0, 0, 0, 0], 
    #         [-1,0, 0, 7, 0, 0, 0, 0, 0], 
    #         [4, 0, -1,0, 2, 0, 0, 0, 5], 
    #         [0, -1,3, 0, 0, 5, 0, 0, -1], 
    #         [0, 0, 4, 0, -1,0, 2, 0, 0], 
    #         [0, 7, 0, 0, 0, 6, 0, 5, 0], 
    #         [0, 3, 0, 0, 0, 5, 0, 0, 5]]

    for y in range(0, 9):
        for x in range(0, 9):
            val = board[y][x]
            Cell.board[y][x] = Cell(x, y, val if val else -10)
            if val > 0:
                CELLS.append(Cell.board[y][x])
    
    print(Cell.board)
    print(np.array([[elem.freedom if hasattr(elem, 'freedom') else -(elem.state != -10) for elem in arr] for arr in Cell.board]))

def ScanBoard():
    #screen = Image.open('screen.png')
    gui.click(1040, 590)
    while (not gui.pixelMatchesColor(787, 980, (150, 150, 150), tolerance = 25) and gui.pixelMatchesColor(735, 980, (150, 150, 150), tolerance = 25)) or not (gui.pixelMatchesColor(925, 135, (50, 50, 50), tolerance = 25) and gui.pixelMatchesColor(925, 160, (50, 50, 50), tolerance = 25)):
        time.sleep(0.0001)
    benchmark()

    #screen = gui.screenshot("screen.png", region = (704 - width / 2, 301 - width / 2, X[8] + width, Y[8] + width))
    screen = gui.screenshot(region = (704 - width / 2, 301 - width / 2, X[8] + width, Y[8] + width))
    for y in range(9):
        for x in range(9):
            pixel = screen.getpixel((X[x], Y[y]))
            if pixel[0] == 255:
                Cell.board[y][x] = Cell(x, y, -1)
                continue
            if pixel > (230, 230, 230):
                Cell.board[y][x] = Cell(x, y, -10)
                continue
            for number in range(1, 10):
                if gui.locate(str(number) + '.png', screen, region = (X[x], Y[y], width, width), confidence = 0.85):
                    Cell.board[y][x] = Cell(x, y, number)
                    CELLS.append(Cell.board[y][x])
                    break

    #print(Cell.board)
    #print(np.array([[elem.freedom if hasattr(elem, 'freedom') else -(elem.state != -10) for elem in arr] for arr in Cell.board]))

def horzClustering():
    print("horzClustering")
    count = 0
    for y in range(0, 9):
        for x in range(0, 10):
            if x != 9 and Cell.board[y][x].state > 0:
                count += 1
            elif count:
                arr = Cell.board[y][x - count:x]
                horzLim = min([elem.freedom for elem in arr])
                for i, elem in enumerate(arr):
                    elem.values[0], elem.values[1] = i, count - 1 - i
                    elem.limits[0] = elem.limits[1] = horzLim
                count = 0
    #print(np.array([[elem.limits[0] if hasattr(elem, 'limits') else 0 for elem in arr] for arr in Cell.board]))

def vertClustering():
    print("vertClustering")
    count = 0
    for x in range(0, 9):
        for y in range(0, 10):
            if y != 9 and Cell.board[y][x].state > 0:
                count += 1
            elif count:
                arr = Cell.board[y - count:y:,x]
                vertLim = min([elem.freedom for elem in arr])
                for i, elem in enumerate(arr):
                    elem.values[2], elem.values[3] = i, count - 1 - i
                    elem.limits[2] = elem.limits[3] = vertLim
                count = 0
    #print(np.array([[elem.limits[2] if hasattr(elem, 'limits') else 0 for elem in arr] for arr in Cell.board]))

def ActivateNumberedCells():
    print("ActivateNumberedCells")
    for cell in CELLS:
        cell.init()

    #print(np.array([[elem.freedom if hasattr(elem, 'freedom') else -(elem.state != -10) for elem in arr] for arr in Cell.board]))

def solve():
    print("solve")
    Cell.condition = True
    while Cell.condition:
        Cell.condition = False
        for cell in CELLS:
            cell.predict()
    #print(Cell.board)

def simulate():
    print("simulate")
    for row, arr in enumerate(Cell.board):
        for col, elem in enumerate(arr):
            if elem.state <= -1:
                gui.doubleClick(X[col] + 704, Y[row] + 301)
            elif elem.state == 0:
                gui.click(X[col] + 704, Y[row] + 301)

def benchmark():
    global Time
    diff = time.time() - Time
    print("time elapsed", diff)
    Time = time.time()
    return diff

width = 25
Time = time.time()
X, Y = [], []
gui.PAUSE = 0.002

CreateGrid()
print("Press 'ENTER' to start the program")
keyboard.wait('ENTER')

for temp in range(9):
    CELLS = []
    total = 0
    
    ScanBoard()
    total += benchmark()
    horzClustering()
    vertClustering()
    ActivateNumberedCells()
    solve()
    total += benchmark()
    simulate()
    total += benchmark()

    print("total time", total)
    time.sleep(3)
    if gui.pixelMatchesColor(787, 980, (150, 150, 150), tolerance = 25):
        gui.click(787, 980)
        sys.exit
    else:
        while not gui.pixelMatchesColor(735, 980, (150, 150, 150), tolerance = 25):
            time.sleep(0.0001)