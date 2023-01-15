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

# unit testing here

def CreateGrid():
    print("CreateGrid")
    for index in range(9):
        X.append(round(59.125 * index + 704.4))
        Y.append(round(59.25 * index + 301.4))
    
    print(X)
    print(Y)

def CreateBoard():
    print("CreateBoard")
    for y in range(0, 9):
        for x in range(0, 9):
            val = board[y][x]
            Cell.board[y][x] = Cell(x, y, val if val else -10)
            if val > 0:
                NumberedCells.append(Cell.board[y][x])
    print(Cell.board)

    # Cell.board[7][2].printInactive()
    # Cell.board[5][0].printInactive()
    # Cell.board[0][4].printInactive()
    # Cell.board[6][8].printInactive()
    # Cell.board[8][4].printInactive()

def horzClustering():
    print("horzClustering")
    for y in range(0, 9):
        count = 0
        for x in range(0, 10):
            if x != 9 and Cell.board[y][x].state > 0:
                count += 1
            elif count:
                arr = Cell.board[y][x - count:x]
                horzLim = min([elem.freedom - (count - 1) for elem in arr])
                for i, elem in enumerate(arr):
                    elem.leftVal = i
                    elem.rightVal = count - 1 - i
                    elem.freedom -= count - 1
                    elem.horzLim = horzLim
                count = 0
    print(np.array([[elem.horzLim if hasattr(elem, 'horzLim') else 0 for elem in arr] for arr in Cell.board]))

def vertClustering():
    print("vertClustering")
    for x in range(0, 9):
        count = 0
        for y in range(0, 10):
            if y != 9 and Cell.board[y][x].state > 0:
                count += 1
            elif count:
                arr = Cell.board[y - count:y:,x]
                vertLim = min([elem.freedom - (count - 1) for elem in arr])
                for i, elem in enumerate(arr):
                    elem.topVal = i
                    elem.bottomVal = count - 1 - i
                    elem.freedom -= count - 1
                    elem.vertLim = vertLim
                count = 0
    print(np.array([[elem.vertLim if hasattr(elem, 'vertLim') else 0 for elem in arr] for arr in Cell.board]))

def ActivateNumberedCells():
    print("ActivateNumberedCells")
    # NumberedCells[6].init() # primarily 0 and 6
    for cell in NumberedCells:
        cell.init()

    # Cell.board[1][3].printActive()
    # Cell.board[0][5].printActive()
    # Cell.board[4][0].printActive()
    # Cell.board[8][8].printActive()

def solve():
    for cell in NumberedCells:
        cell.predict()
    print(Cell.board)

X, Y = [], []
CreateGrid()

width = 25
shifts = [] #advanced pixel comparisons
blues = []
# screen = Image.open('screen.png')

#print("Press 'ENTER' to start the program")
#keyboard.wait('ENTER')
# screen = pyautogui.screenshot('screen.png', region = (470, 475))
# pyautogui.screenshot('The One.png', region = (942 - width / 2, 539 - width / 2, width, width))

NumberedCells = []
board = [[0, 0, 0, 0, 0, 6, 9, -1,0], 
         [5, 0, 0, 6, 0, 0, 0, 3, 0], 
         [5, 0, 0, 0, -1,0, 0, 0, 0], 
         [-1,0, 0, 7, 0, 0, 0, 0, 0], 
         [4, 0, -1,0, 2, 0, 0, 0, 5], 
         [0, -1,3, 0, 0, 5, 0, 0, -1], 
         [0, 0, 4, 0, -1,0, 2, 0, 0], 
         [0, 7, 0, 0, 0, 6, 0, 5, 0], 
         [0, 3, 0, 0, 0, 5, 0, 0, 5]]
print(board)

CreateBoard()
horzClustering()
vertClustering()
print(np.array([[0 if elem.freedom == -10 else elem.freedom for elem in arr] for arr in Cell.board]))
ActivateNumberedCells()
solve()

#pyautogui.click(100, 200)
#pyautogui.doubleClick(100, 200)