import numpy as np

"""
-10 is blank
-1 is red
0 is blue
1-9 is number
r is red/locked
g is gray/blank
"""

inverse = [1, 0, 3, 2]
class Cell:
    board = np.full([9, 9], None) # (y, x). read left to right, top to bottom. 
    predictions = set()

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.freedom = self.state = state
        self.left, self.right, self.top, self.bottom = [], [], [], []
        self.values = [0, 0, 0, 0]

        # link cells together and lets them view numbered cells in the cardinal directions
        if self.state != -1:
            AdjacentLeft = Cell(0, 0, -1) if self.x == 0 else Cell.board[self.y][self.x - 1]
            if AdjacentLeft.state < 0:
                self.right = AdjacentLeft.right
            if self.state > 0:
                self.left = [self] + AdjacentLeft.left
                for elem in self.left:
                    elem.right.append(self)
            else:
                self.left = AdjacentLeft.left

            AdjacentTop = Cell(0, 0, -1) if self.y == 0 else Cell.board[self.y - 1][self.x]
            if AdjacentTop.state < 0:
                self.bottom = AdjacentTop.bottom
            if self.state > 0:
                self.top = [self] + AdjacentTop.top
                for elem in self.top:
                    elem.bottom.append(self)
            else:
                self.top = AdjacentTop.top

    def __repr__(self):
        return str(self.state) if self.state >= 0 else ('r' if self.state == -1 else 'g')

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def printActive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}, freedom: {self.freedom}")
        print(f"horzLim: {self.horzLim}, vertLim: {self.vertLim}")
        print(f"leftVal: {self.leftVal}, {[elem.x for elem in self.left]}")
        print(f"rightVal: {self.rightVal}, {[elem.x for elem in self.right]}")
        print(f"topVal: {self.topVal}, {[elem.y for elem in self.top]}")
        print(f"bottomVal: {self.bottomVal}, {[elem.y for elem in self.bottom]}")

    def printInactive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}")
        print(f"left: {self.left}")
        print(f"right: {self.right}")
        print(f"top: {self.top}")
        print(f"bottom: {self.bottom}")

    def init(self):
        self.limits = [10, 10, 10, 10]
        self.values = [self.leftVal, self.rightVal, self.topVal, self.bottomVal] # remove later
        self.left, self.right, self.top, self.bottom = [Cell.board[self.y][max(0, self.x - (self.leftVal + self.horzLim)):self.x][::-1].tolist(), 
                                                        Cell.board[self.y][self.x + 1:self.x + 1 + (self.rightVal + self.horzLim)].tolist(), 
                                                        Cell.board[max(0, self.y - (self.topVal + self.vertLim)):self.y,self.x][::-1].tolist(), 
                                                        Cell.board[self.y + 1:self.y + 1 + (self.bottomVal + self.vertLim),self.x].tolist()]

        # slice list when reaching a barrier or when overstepping
        # there are two variables named i. conflicting data
        for index, arr in enumerate([self.left, self.right, self.top, self.bottom]):
            for i, elem in enumerate(arr):
                if -1 <= elem.state <= i:
                    del arr[i - (elem.state != -1):]
                    self.limits[index] = len(arr)
                    break

    # affect cells which it can "see" and adds them to the prediction list/set
    def affect(self):
        for i, arr in enumerate([self.right, self.left, self.bottom, self.top]):
            for elem in arr:
                if self.state == -1:
                    mat = [elem.left, elem.right, elem.top, elem.bottom]
                    hi = mat[i][elem.limits[i]:]
                    if hi != []:
                        Cell.predictions.add(elem)
                        if i < 2:
                            hi.limits[1] = self.x + (i == 0) * hi.x
                        else:
                            hi.limits[1] = self.y + (i == 0) * hi.y
                elif self.state == 0:
                    if i < 2:
                        value = self.x + (i == 0) * hi.x
                    else:
                        value = self.y + (i == 0) * hi.y

                    if value == elem.values[i]:
                        Cell.predictions.add(elem)

    def markRed(self):
        if self.state == -10:
            self.state = -1
            self.affect()
            return True
        return False

    def markBlue(self):
        if self.state == -10:
            self.state = 0
            self.affect()
            return True
        return False

    # should call this update
    # source cell may be out of range of the target cell because it connects to a cluster which interferes by possibly creating overstepping for the target cell
    def update(self):
        mat = [self.left[self.leftVal:self.leftVal + self.freedom], self.right[self.rightVal:self.freedom], self.top[self.topVal:self.freedom], self.bottom[self.bottomVal:self.freedom]]
        for i, arr in enumerate(mat):
            for count, elem in enumerate(arr):
                if elem.state < 0:
                    break
                self.freedom -= count
                self.values[i] += count
            self.limits = [min(elem, self.freedom) for elem in self.limits]

    # create a direction function which directly passes the index. 
    def predict(self):
        # Each numbered cell has 24 permuations for the order of completing the 4 cardinal directions
        # loop this until not WithinRange, or for a better description: no change to freedom or left/right/top/bottom states? 
        whatever = True
        while whatever:
            self.update()
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = len(self.left) + len(self.right) + len(self.top) + len(self.bottom) - self.state
            diff = self.leftLim + self.rightLim + self.topLim + self.bottomLim - self.state
            mat = [self.left[self.leftVal:-diff], self.right[self.rightVal:-diff], self.top[self.topVal:-diff], self.bottom[self.bottomVal:-diff]]
            for i, arr in enumerate([self.left[self.leftVal:], self.right[self.rightVal:], self.top[self.topVal:], self.bottom[self.bottomVal:]]):
                for count, elem in enumerate(arr):
                    if elem.state < 0 and count > len(arr) - diff:
                        break
                    elem.markBlue() # does marking blue connect to secondary clusters? prep current cell for if it can see all its dots from connecting to secondary clusters

                self.freedom -= count
                match i:
                    case 0:
                        self.leftVal += count
                    case 1:
                        self.rightVal += count
                    case 2: 
                        self.topVal += count
                    case 3: 
                        self.bottomVal += count

            # This number can see all its dots
            # Looking further in one direction would exceed this number
            if sum([elem.state >= 0 for elem in self.left[self.leftVal + 1:self.freedom + self.leftVal + 1]]) == self.freedom:
                self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.right[self.rightVal + 1:self.freedom + self.rightVal  + 1]]) == self.freedom:
                self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.top[self.topVal + 1:self.freedom + self.topVal + 1]]) == self.freedom:
                self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.bottom[self.bottomVal + 1:self.freedom + self.bottomVal + 1]]) == self.freedom:
                whatever = self.left[self.leftVal].markRed()

            Cell.predictions.discard(self)