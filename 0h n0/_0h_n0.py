from Cell import Cell
import cv2 # for confidence parameter
import keyboard
import numpy as np
import pyautogui
import time

def CreateGrid():
    print("CreateGrid")
    for index in range(9):
        X.append(round(59.125 * index + 704.4))
        Y.append(round(59.25 * index + 301.4))
    
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
                NumberedCells.append(Cell.board[y][x])
    
    print(Cell.board)
    print(np.array([[elem.freedom if hasattr(elem, 'freedom') else -(elem.state != -10) for elem in arr] for arr in Cell.board]))

def ScanBoard():
    #screen = Image.open('screen.png')
    width = 20
    print("Press 'ENTER' to start the program")
    keyboard.wait('ENTER')

    pyautogui.click(1040, 590)
    while not pyautogui.pixelMatchesColor(925, 130, (129, 129, 129)):
        time.sleep(0.00001)
    benchmark()

    screen = pyautogui.screenshot(region = (X[0] - width / 2, Y[0] - width / 2, X[8] - X[0] + width, Y[8] - Y[0] + width))
    for y in range(9):
        for x in range(9):
            pixel = screen.getpixel((X[x] - X[0], Y[y] - Y[0]))
            if pixel == (239, 239, 239):
                Cell.board[y][x] = Cell(x, y, -10)
                continue
            elif pixel == (255, 68, 86):
                Cell.board[y][x] = Cell(x, y, -1)
                continue
            for number in range(1, 10):
                if pyautogui.locate(str(number) + '.png', screen, region = (X[x] - X[0], Y[y] - Y[0], width, width), confidence = 0.85):
                    Cell.board[y][x] = Cell(x, y, number)
                    NumberedCells.append(Cell.board[y][x])
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
    for cell in NumberedCells:
        cell.init()

    #print(np.array([[elem.freedom if hasattr(elem, 'freedom') else -(elem.state != -10) for elem in arr] for arr in Cell.board]))

def solve():
    print("solve")
    condition = 2
    while condition:
        if Cell.predictions:
            temp = Cell.predictions
            Cell.predictions = set()
        else:
            temp = NumberedCells
            condition -= 1

        for cell in temp:
            cell.predict()
    #print(Cell.board)

def simulate():
    print("simulate")
    for arr in Cell.board:
        for elem in arr:
            x, y = X[elem.x], Y[elem.y]
            if elem.state <= -1:
                pyautogui.doubleClick(x, y)
            elif elem.state == 0:
                pyautogui.click(x, y)

def benchmark():
    global Time
    diff = time.time() - Time
    print("time elapsed", diff)
    Time = time.time()
    return diff

Time = time.time()
total = 0
X, Y = [], []
NumberedCells = []
pyautogui.PAUSE = 0.002

CreateGrid()
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