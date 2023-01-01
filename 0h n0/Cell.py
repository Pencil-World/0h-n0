import numpy as np


"""
None is blank
Negative is red
Zero is blue
Positive is number

Logic:
There are 24 permuations for the order of filling out the 4 cardinal directions for each numbered cell
This number can see all its dots
One specific dot is included in all solutions imaginable
Only one direction remains for this number to look in
Looking further in one direction would exceed this number
"""

class Cell:
    board = np.full([9, 9], None)
    PostPredict = {} # unnecessary
    UpdateCell = None # its important to keep track of last updated cell becuase the predicted cells in the following might not be predicted. each numbered cell has a range

    # read left to right, top to bottom
    def __init__(self, x, y, state = None):
        self.x = x
        self.y = y
        self.state = state
        self.leftVal = self.rightVal = self.topVal = self.bottomVal = 0 # called leftMin and leftMax?
        self.left, self.right, self.top, self.bottom = [[], [], [], []]
        AdjacentLeft = Cell.board[self.x - 1][self.y]
        AdjacentTop = Cell.board[self.x][self.y - 1]
        
        if self.state != -1:
            # update the numbered cells blank cells view
            if self.x > 0:
                self.right = AdjacentLeft.right
                self.left = [AdjacentLeft] + AdjacentLeft.left if AdjacentLeft.state > 0 else AdjacentLeft.left
            if self.y > 0:
                self.bottom = AdjacentTop.bottom
                self.top = [AdjacentTop] + AdjacentTop.top if AdjacentTop.state > 0 else AdjacentTop.top

            # update cardinal direction values of contiguous numbered cells
            if self.state > 0:
                self.horzLim = self.state
                if self.x > 0:
                    AdjacentLeft.right.append(self)
                    for i, item in enumerate(self.left):
                        if item.x != self.x - i - 1
                            break
                        self.rightVal += 1
                        item.leftVal += 1
                self.vertLim = self.state
                if self.y > 0:
                    AdjacentTop.bottom.append(self)
                    for i, item in enumerate(self.top):
                        if item.y != self.y - i - 1
                            break
                        self.bottomVal += 1
                        item.topVal += 1

    def __repr__(self):
        return str(self.state if self.state else 0)

    def init(self):
        self.left, self.right, self.top, self.bottom = [[], [], [], []] # important to clear the clutter in numbered cells from the constructor
        #leftLim = rightLim = self.vertLim
        for i in range(self.horzLim - self.leftVal):
            cell = Cell.board[self.x - i][self.y]
            if cell.state > 0 and cell.state < len(self.left):
                self.left.remove(i - 1)
                break
            else:
                self.left.append(cell)

    #def initRed(self):
    #    for item in Cell.board[self.y][:self.x:-1]:
    #        if item.state == -1:
    #            break
    #        if item.state != 0:
    #            item.RIGHT = Cell.board[self.y][item.x + 1:self.x]
    #    for item in Cell.board[self.y][self.x + 1:]:
    #        if item.state == -1:
    #            break
    #        if item.state != 0:
    #            item.LEFT = Cell.board[self.y][self.x + 1:item.x:-1]
    #    for item in Cell.board[:self.y:-1,self.x]:
    #        if item.state == -1:
    #            break
    #        if item.state != 0:
    #            item.BOTTOM = Cell.board[item.y + 1:self.y,self.x]
    #    for item in Cell.board[self.y + 1:,self.x]:
    #        if item.state == -1:
    #            break
    #        if item.state != 0:
    #            item.TOP = Cell.board[self.y + 1:item.y,self.x:-1]

    #def initBlue(self):
    #    if not self.LEFT:
    #        self.LEFT = Cell.board[self.y][:self.x:-1]
    #    if not self.RIGHT:
    #        self.RIGHT = Cell.board[self.y][self.x + 1:]
    #    if not self.TOP:
    #        self.TOP = Cell.board[:self.y,self.x:-1]
    #    if not self.BOTTOM:
    #        self.BOTTOM = Cell.board[self.y + 1:,self.x]

    #    # readjust value of 'state' if there are adjacent number cells
    #    Cell.board[self.x - 1][self.y] -= 1

    #    if not self.right:
    #        temp = np.array([self])
    #        for stuff in self.LEFT:
    #            stuff.right = temp
    #            if stuff.state != 0:
    #                temp = np.append([stuff], temp)
    #    if not self.left:
    #        temp = np.array([self])
    #        for stuff in self.RIGHT:
    #            stuff.left = temp
    #            if stuff.state != 0:
    #                temp = np.append(temp, [stuff])
    #    if not self.bottom:
    #        temp = np.array([self])
    #        for stuff in self.TOP:
    #            stuff.bottom = temp
    #            if stuff.state != 0:
    #                temp = np.append([stuff], temp)
    #    if not self.top:
    #        temp = np.array([self])
    #        for stuff in self.BOTTOM:
    #            stuff.top = temp
    #            if stuff.state != 0:
    #                temp = np.append(temp, [stuff])

    def update(self, state, direction):# direction is excluded. direction of original signalling cell
        self.state = state
        # affect cells which it can "see" and predicts for them
        if direction == "left":
            for arr in [item.right, item.top, item.bottom]: # test if references or not to prevent overcopying
                for stuff in arr:
                    stuff.predict(self)

    def markRed(self):
        self.state = -1
        update()

    def markBlue(self):
        self.state = 0
        update()

    def predict(self, cell):
        freedom = self.state - (self.leftVal + self.rightVal + self.topVal + self.bottomVal)
        if freedom == 0:
            # This number can see all its dots
            self.left[self.leftVal].markRed()
            self.left[self.leftVal].markRed()
            self.left[self.leftVal].markRed()
            self.left[self.leftVal].markRed()
        else:
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = len(self.left) + len(self.right) + len(self.top) + len(self.bottom) - self.state
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, item in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        item.markBlue()
                    elif item.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            self.state -= diff - self.leftVal # important
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, item in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        item.markBlue()
                    elif item.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, item in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        item.markBlue()
                    elif item.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, item in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        item.markBlue()
                    elif item.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break

            # Looking further in one direction would exceed this number
            sum(cell.state > 0 for cell in self.left[self.leftVal:freedom])