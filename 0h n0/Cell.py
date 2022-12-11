import numpy as np

class Cell:
    board = np.full([9, 9], None)
    PostPredict = []

    def __init__(self, x, y, state = None):
        self.x = x
        self.y = y
        self.state = state
        self.left = self.right = self.top = self.bottom = None

    def initRed(self):# switch to mark() function
        # change to item.predict()
        temp = None
        for item in Cell.board[self.y][:self.x:-1]:
            if item.state == -1:
                break
            if item.state != 0:
                item.initBlue(temp, self.x, self.y)
                temp = item
        for item in Cell.board[self.y][self.x + 1:]:
            if item.state == -1:
                break
            if item.state != 0:
                item.initBlue(self.x, self.y)
        for item in Cell.board[:self.y:-1,self.x]:
            if item.state == -1:
                break
            if item.state != 0:
                item.initBlue(self.x, self.y)
        for item in Cell.board[self.y + 1:,self.x]:
            if item.state == -1:
                break
            if item.state != 0:
                item.initBlue(self.x, self.y)

    def initBlue(self, x = None, y = None):
        self.left = []
        self.right = []
        self.top = []
        self.bottom = []
        # remove?
        for item in Cell.board[self.y][:self.x:-1]:
            if item.state == -1:
                break
            if item.state > 0:
                self.left.append(item)
        for item in Cell.board[self.y][self.x + 1:]:
            if item.state == -1:
                break
            if item.state > 0:
                self.right.append(item)
        for item in Cell.board[:self.y:-1,self.x]:
            if item.state == -1:
                break
            if item.state > 0:
                self.top.append(item)
        for item in Cell.board[self.y + 1:,self.x]:
            if item.state == -1:
                break
            if item.state > 0:
                self.bottom.append(item)

        if x:
            if x < self.x:
                self.left = Cell.board[self.y][x + 1:self.x]
                self.left = temp.left + temp
            else:
                self.right = Cell.board[self.y][self.x + 1:x]
        else:
            if y < self.y:
                self.top = Cell.board[y + 1:self.y,self.x]
            else:
                self.bottom = Cell.board[self.y + 1:y,self.x]

    def hi(self):
        if not self.left:
            self.left = [item for item in Cell.board[self.y][:self.x] if item.state != 0]
            self.left = Cell.board[self.y][:self.x]
        if not self.right:
            self.right = Cell.board[self.y][self.x + 1:]
        if not self.top:
            self.top = Cell.board[:self.y,self.x]
        if not self.bottom:
            self.bottom = Cell.board[self.y + 1:,self.x]

    def __str__(self):
        return str(self.state)

    def markRed(self):
        self.state = -1
        # switch to mark() function
        # init red but change to item.predict()

    def markBlue(self):
        self.state = 0

    def predict(self):
        if not self.left:
            self.left = Cell.board[self.y][:self.x]
        if not self.right:
            self.right = Cell.board[self.y][self.x + 1:]
        if not self.top:
            self.top = Cell.board[:self.y,self.x]
        if not self.bottom:
            self.bottom = Cell.board[self.y + 1:,self.x]
        return
    
    def print():
        print(np.array([[elem.state if elem.state else 0 for elem in item] for item in Cell.board]))