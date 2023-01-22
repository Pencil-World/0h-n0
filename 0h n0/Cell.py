import numpy as np

"""
-10 is blank
-1 is red
0 is blue
1-9 is number
r is red/locked
g is gray/blank
"""

class Cell:
    board = np.full([9, 9], None) # (y, x). read left to right, top to bottom. 
    predictions = set()

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.left, self.right, self.top, self.bottom = [], [], [], []

        if self.state != -1:
            # link cells together and lets them view numbered cells in the cardinal directions
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

                # adjusts freedom according to connected numbered cells
                for i, arr in enumerate([self.left[1:], self.top[1:]]):
                    for count, elem in enumerate(arr, 1):
                        if [self.x - elem.x, self.y - elem.y][i] != count:
                            count -= 1
                            break
                        elem.freedom -= 1
                    self.freedom -= count if arr else 0
            else:
                self.left = AdjacentLeft.left
                self.top = AdjacentTop.top

    def __repr__(self):
        return str(self.state) if self.state >= 0 else ('+' if self.state == -1 else '-')

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def printActive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}, freedom: {self.freedom}")
        print(f"leftVal: {self.values[0]}, leftLim: {self.limits[0]}, {[elem.x for elem in self.left]}")
        print(f"rightVal: {self.values[1]}, rightLim: {self.limits[1]}, {[elem.x for elem in self.right]}")
        print(f"topVal: {self.values[2]}, topLim: {self.limits[2]}, {[elem.y for elem in self.top]}")
        print(f"bottomVal: {self.values[3]}, bottomLim: {self.limits[3]}, {[elem.y for elem in self.bottom]}")

    def printInactive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}")
        print(f"left: {self.left}")
        print(f"right: {self.right}")
        print(f"top: {self.top}")
        print(f"bottom: {self.bottom}")

    def init(self):
        self.left, self.right, self.top, self.bottom = [Cell.board[self.y][max(0, self.x - (1 + self.values[0] + self.limits[0])):self.x][::-1].tolist(), 
                                                        Cell.board[self.y][self.x + 1:self.x + 1 + (1 + self.values[1] + self.limits[1])].tolist(), 
                                                        Cell.board[max(0, self.y - (1 + self.values[2] + self.limits[2])):self.y,self.x][::-1].tolist(), 
                                                        Cell.board[self.y + 1:self.y + 1 + (1 + self.values[3] + self.limits[3]),self.x].tolist()]

        # 2, 2 -, 2 - 1, 2 - +, 2 - - 9, 2 - - +
        # slice list when reaching a barrier (red) or when overstepping (numbered)
        for i, arr in enumerate([self.left, self.right, self.top, self.bottom]):
            for count, elem in enumerate(arr, 1):
                if -1 <= elem.state < count or count == 1 + self.values[i] + self.limits[i]:
                    count -= 1 + (0 < elem.state)
                    break
            self.limits[i] = count if arr else 0

    # affect cells which it can "see" and adds them to the prediction list/set
    def affect(self):
        for i, arr in enumerate([self.right, self.left, self.bottom, self.top]):
            for elem in arr:
                diff = [elem.x - self.x, self.x - elem.x, elem.y - self.y, self.y - elem.y][i] - 1
                if diff <= elem.limits[i]: # just less than?
                    Cell.predictions.add(elem)
                    if self.state == -1:
                        elem.limits[i] = diff
                        
    def markRed(self):
        if self.state == -10:
            #print(f"markRed: ({self.y}, {self.x})")
            self.state = -1
            self.affect()
            return True
        return False

    def markBlue(self):
        if self.state == -10:
            #print(f"markBlue: ({self.y}, {self.x})")
            self.state = 0
            self.affect()
            return True
        return False

    def predict(self):
        # Each numbered cell has 24 permuations for the order of completing the 4 cardinal directions
        # loop until predict() stops marking
        if self.freedom:
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = sum(self.limits) - self.state
            for i, temp in enumerate([self.left, self.right, self.top, self.bottom]):
                self.limits[i] = min(self.values[i] + self.freedom, self.limits[i])
                arr = temp[self.values[i]:self.limits[i]]
                if arr:
                    for count, elem in enumerate(arr, 1):
                        # if marking blue connects the numbered cell to a secondary cluster
                        if elem.state < 0 and self.limits[i] - self.values[i] - diff < count:
                            count -= 1
                            break
                        elem.markBlue()

                    self.freedom -= count
                    self.values[i] += count

            # This number can see all its dots
            # Looking further in one direction would exceed this number
            # cannot mark red dots off the board
            for i, arr in enumerate([self.left, self.right, self.top, self.bottom]):
                if len(arr) > self.values[i] and sum([elem.state >= 0 for elem in arr[self.values[i] + 1:self.freedom + 1]]) == self.freedom:
                    arr[self.values[i]].markRed()