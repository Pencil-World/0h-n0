import numpy as np


"""
-10 is blank
-1 is red
0 is blue
1-9 is number
"""

class Cell:
    board = np.full([9, 9], None) # (y, x)
    predictions = {} # unnecessary
    UpdateCell = None # its important to keep track of last updated cell becuase the predicted cells in the following might not be predicted. each numbered cell has a range
    # update cell is redundant because pass self to predict functions

    # read left to right, top to bottom
    def __init__(self, x, y, state = None):
        self.x = x
        self.y = y
        self.state = state
        self.leftVal = self.rightVal = self.topVal = self.bottomVal = 0
        self.left, self.right, self.top, self.bottom = [[], [], [], []]
        AdjacentLeft = Cell.board[self.x - 1][self.y]
        AdjacentTop = Cell.board[self.x][self.y - 1]
        
        if self.state != -1:
            if self.x > 0:
                self.right = AdjacentLeft.right
                self.left = [AdjacentLeft] + AdjacentLeft.left if AdjacentLeft.state > 0 else AdjacentLeft.left
            if self.y > 0:
                self.bottom = AdjacentTop.bottom
                self.top = [AdjacentTop] + AdjacentTop.top if AdjacentTop.state > 0 else AdjacentTop.top

            if self.state > 0:
                if self.x > 0:
                    AdjacentLeft.right.append(self)
                if self.y > 0:
                    AdjacentTop.bottom.append(self)

    def __repr__(self):
        return str(self.state if self.state else 0)

    def init(self):
        self.right = self.right[:-1]
        self.bottom = self.bottom[:-1]
        self.left, self.right, self.top, self.bottom = [Cell.board[self.y][self.x:self.horzLim - self.leftVal:-1], 
                                                        Cell.board[self.y][self.x + 1:self.horzLim - self.rightVal], 
                                                        Cell.board[self.x:self.horzLim - self.leftVal:-1][self.y], # fix
                                                        Cell.board[self.x:self.horzLim - self.leftVal:][self.y]]

        for arr in [self.left, self.right, self.top, self.bottom]:
            for i, cell in enumerate(arr):
                if cell.state > 0 and cell.state < len(arr):
                    del arr[i - 1:]
                    break

    def update(self, direction = None):
        # affect cells which it can "see" and predicts for them
        # test if references or not to prevent overcopying
        mat = None
        match direction:
            case "left" | "right":
                mat = [self.top, self.bottom]
            case "top" | "bottom":
                mat = [self.left, self.right]
            case other:
                mat = [self.left[0].left, self.right[0].right, self.top[0].top, self.bottom[self.bottomVal].bottom] # hmm not sure what to do here. have left and LEFT because what if there are continuouse number slots, we need to account for those

        for arr in mat:
            for cell in arr:
                cell.predict(self)

    def markRed(self, direction):
        self.state = -1
        update(direction)

    def markBlue(self, direction):
        self.state = 0
        update(direction)

    # Each numbered cell has 24 permuations for the order of filling out the 4 cardinal directions
    # This number can see all its dots
    # One specific dot is included in all solutions imaginable
    # Only one direction remains for this number to look in
    # Looking further in one direction would exceed this number
    def predict(self, cell):
        # update state/leftVal/topVal
        # update left and right to check of overstepping
        if cell.x > self.x - len(self.left):
            return
        if cell.x == self.x - leftVal:
            return

        freedom = self.state - (self.leftVal + self.rightVal + self.topVal + self.bottomVal) # set in init? or in main?
        if freedom == 0:
            # This number can see all its dots
            self.left[self.leftVal].markRed("left")
            self.right[self.rightVal].markRed("right")
            self.top[self.topVal].markRed("top")
            self.bottom[self.bottomVal].markRed("bottom")
            self.update()
        else:
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = len(self.left) + len(self.right) + len(self.top) + len(self.bottom) - self.state
            if self.leftValue < diff:
                for index, elem in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        elem.markBlue()
                    elif elem.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            self.state -= diff - self.leftVal # important

            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, elem in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        elem.markBlue()
                    elif elem.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, elem in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        elem.markBlue()
                    elif elem.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break
            if self.state < self.left[0].leftValue:
                # check all directions to see if the cell will over step. if it does, then markRed()
                self.left[0].markRed()
            if self.leftValue < diff:
                for index, elem in enumerate(self.left[self.leftVal:]):
                    if index < diff:
                        elem.markBlue()
                    elif elem.state >= 0:
                        self.state += 1
                    else:# state is -1 or None
                        break

            # Looking further in one direction would exceed this number
            if sum(elem.state > 0 for elem in self.left[self.leftVal + 1:freedom + self.leftVal + 1] == freedom:
                self.left[self.leftVal].markRed("left")
            if sum(elem.state > 0 for elem in self.left[self.leftVal:freedom + 1]) == freedom:
                self.left[self.leftVal].markRed("left")
            if sum(elem.state > 0 for elem in self.left[self.leftVal:freedom + 1]) == freedom:
                self.left[self.leftVal].markRed("left")
            if sum(elem.state > 0 for elem in self.left[self.leftVal:freedom + 1]) == freedom:
                self.left[self.leftVal].markRed("left")