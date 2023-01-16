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
        self.state = state
        self.left, self.right, self.top, self.bottom = [], [], [], []

        # link cells together and lets them view numbered cells in the cardinal directions
        if self.state != -1:
            AdjacentLeft = Cell(0, 0, -1) if self.x == 0 else Cell.board[self.y][self.x - 1]
            if AdjacentLeft.state < 0:
                self.right = AdjacentLeft.right
            AdjacentTop = Cell(0, 0, -1) if self.y == 0 else Cell.board[self.y - 1][self.x]
            if AdjacentTop.state < 0:
                self.bottom = AdjacentTop.bottom

            if self.state > 0:
                self.freedom = state
                self.values, self.limits = [None] * 4, [None] * 4

                self.left = [self] + AdjacentLeft.left
                for elem in self.left:
                    elem.right.append(self)
                self.top = [self] + AdjacentTop.top
                for elem in self.top:
                    elem.bottom.append(self)
            else:
                self.left = AdjacentLeft.left
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
        print(f"horzLim: {self.limits[0]}, vertLim: {self.limits[3]}")
        print(f"leftVal: {self.values[0]}, {[elem.x for elem in self.left]}")
        print(f"rightVal: {self.values[1]}, {[elem.x for elem in self.right]}")
        print(f"topVal: {self.values[2]}, {[elem.y for elem in self.top]}")
        print(f"bottomVal: {self.values[3]}, {[elem.y for elem in self.bottom]}")

    def printInactive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}")
        print(f"left: {self.left}")
        print(f"right: {self.right}")
        print(f"top: {self.top}")
        print(f"bottom: {self.bottom}")

    def init(self):
        self.left, self.right, self.top, self.bottom = [Cell.board[self.y][max(0, self.x - (self.values[0] + self.limits[0])):self.x][::-1].tolist(), 
                                                        Cell.board[self.y][self.x + 1:self.x + 1 + (self.values[1] + self.limits[1])].tolist(), 
                                                        Cell.board[max(0, self.y - (self.values[2] + self.limits[2])):self.y,self.x][::-1].tolist(), 
                                                        Cell.board[self.y + 1:self.y + 1 + (self.values[3] + self.limits[3]),self.x].tolist()]

        # slice list when reaching a barrier or when overstepping
        # there are two variables named i. conflicting data
        for i, arr in enumerate([self.left, self.right, self.top, self.bottom]):
            for count, elem in enumerate(arr):
                if -1 <= elem.state <= i:
                    del arr[count - (elem.state != -1):]
                    self.limits[i] = len(arr)
                    break

    # affect cells which it can "see" and adds them to the prediction list/set
    def affect(self):
        for i, arr in enumerate([self.right, self.left, self.bottom, self.top]):
            for elem in arr:
                diff = [elem.x - self.x, self.x - elem.x, elem.y - self.y, self.y - elem.y][i]
                if self.state == -1:
                    # if marking red infringes on numbered cell's range
                    if [elem.left, elem.right, elem.top, elem.bottom][i][diff:]:
                        Cell.predictions.add(elem)
                        elem.limits[i] = diff
                elif self.state == 0:
                    # if marking blue changes numbered cell's freedom
                    if diff == elem.values[i]:
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
        # mat = [self.left[self.values[0]:self.leftVal + self.freedom], self.right[self.rightVal:self.freedom], self.top[self.topVal:self.freedom], self.bottom[self.bottomVal:self.freedom]]
        for i, temp in enumerate([self.right, self.left, self.bottom, self.top]):
            arr = temp[self.values[i]:self.values[i] + self.freedom]
            for count, elem in enumerate(arr):
                if elem.state < 0:
                    break
                self.freedom -= count
                self.values[i] += count
            self.limits = [min(elem, self.freedom) for elem in self.limits]

    # create a direction function which directly passes the index. 
    def predict(self):
        # Each numbered cell has 24 permuations for the order of completing the 4 cardinal directions
        # loop until no change to freedom or predict() stops marking
        whatever = True
        while whatever:
            self.update()
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = self.leftLim + self.rightLim + self.topLim + self.bottomLim - self.state
            #mat = [self.left[self.leftVal:], self.right[self.rightVal:], self.top[self.topVal:], self.bottom[self.bottomVal:]]
            #mat = [self.left[self.values[0]:], self.right[self.values[1]:], self.top[self.values[2]:], self.bottom[self.values[3]:]]
            for i, temp in enumerate([self.right, self.left, self.bottom, self.top]):
                arr = temp[self.values[i]:]
                for count, elem in enumerate(arr):
                    # if marking blue connects the numbered cell to a secondary cluster
                    if elem.state < 0 and count > len(arr) - diff:
                        break
                    whatever = elem.markBlue()

                self.freedom -= count
                self.values[i] += count

            # This number can see all its dots
            # Looking further in one direction would exceed this number
            if sum([elem.state >= 0 for elem in self.left[self.leftVal + 1:self.freedom + self.leftVal + 1]]) == self.freedom:
                whatever = self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.right[self.rightVal + 1:self.freedom + self.rightVal  + 1]]) == self.freedom:
                whatever = self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.top[self.topVal + 1:self.freedom + self.topVal + 1]]) == self.freedom:
                whatever = self.left[self.leftVal].markRed()
            if sum([elem.state >= 0 for elem in self.bottom[self.bottomVal + 1:self.freedom + self.bottomVal + 1]]) == self.freedom:
                whatever = self.left[self.leftVal].markRed()

            Cell.predictions.discard(self)