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
    predictions = {}

    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.freedom = self.state = state
        self.left, self.right, self.top, self.bottom = [], [], [], []
        self.horzLim, self.vertLim = [[[10]], [[10]]] # references. can connect horzLim of clusters through one. can change all horzLim of a cluster through one

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
        print(f"leftVal: {self.leftVal}, {[elem.x for elem in self.LEFT]}")
        print(f"rightVal: {self.rightVal}, {[elem.x for elem in self.RIGHT]}")
        print(f"topVal: {self.topVal}, {[elem.y for elem in self.TOP]}")
        print(f"bottomVal: {self.bottomVal}, {[elem.y for elem in self.BOTTOM]}")

    def printInactive(self):
        print()
        print(f"(Y, X): ({self.y}, {self.x}), state: {self.state}")
        print(f"left: {self.left}")
        print(f"right: {self.right}")
        print(f"top: {self.top}")
        print(f"bottom: {self.bottom}")

    def init(self):
        for numbered cells only. create slice copy
        self.left = self.left[1:]
        self.right = self.right[:-1]
        self.top = self.top[1:]
        self.bottom = self.bottom[:-1]

        # replace the funcionalities of self.left with self.LEFT. so self.left, self.right, self.top, self.bottom = [,,,,]
        self.LEFT, self.RIGHT, self.TOP, self.BOTTOM = [Cell.board[self.y][max(0, self.x - (self.leftVal + self.horzLim)):self.x][::-1].tolist(), 
                                                        Cell.board[self.y][self.x + 1:self.x + 1 + (self.rightVal + self.horzLim)].tolist(), 
                                                        Cell.board[max(0, self.y - (self.topVal + self.vertLim)):self.y,self.x][::-1].tolist(), 
                                                        Cell.board[self.y + 1:self.y + 1 + (self.bottomVal + self.vertLim),self.x].tolist()]

        # slice list when reaching a barrier or when overstepping
        for arr in [self.LEFT, self.RIGHT, self.TOP, self.BOTTOM]:
            for i, elem in enumerate(arr):
                if -1 <= elem.state <= i:
                    del arr[i - (elem.state != -1):]
                    break

    def trim(self):
        for arr in [self.LEFT, self.RIGHT, self.TOP, self.BOTTOM]:
            for i, elem in enumerate(arr):
                if -1 <= elem.state <= i:
                    del arr[i - (elem.state != -1):]
                    break
        return

    # affect cells which it can "see" and predicts for them
    # key-value pairs: {0: "left", 1: "right", 2: "top", 3: "bottom"}
    def update(self):
        # match direction:
        #     case "left" | "right":
        #         mat = [self.top, self.bottom]
        #     case "top" | "bottom":
        #         mat = [self.left, self.right]
        #     case other:
        #         mat = [self.LEFT, self.RIGHT, self.TOP, self.BOTTOM]
        # if direction == "0" or direction == "1":
        #     mat = [self.top, self.bottom]
        # elif direction == "2" or direction == "3":
        #     mat = [self.left, self.right]
        # else:
        #     mat = [self.left, self.right, self.top, self.bottom]

        for arr in [self.left, self.right, self.top, self.bottom]:
            for elem in arr:
                Cell.board
                elem.predict()

    def markRed(self):
        if self.state == -10:
            self.state = -1
            update()

    def markBlue(self):
        if self.state == -10:
            self.state = 0
            update()

    # source cell may be out of range of the target cell because it connects to a cluster which interferes by possibly creating overstepping for the target cell
    def WithinRange(self, cell):
        # index = [self.x - self.leftVal < cell.x < self.x, self.x < cell.x < self.x + self.rightVal, 
        #          self.y - self.topVal < cell.y < self.y, self.y < cell.y < self.y + self.bottomVal].index(True) # remove this check
        # if index == -1:
        #     return -1
        index = [cell.x < self.x, self.x < cell.x, cell.y < self.y, self.y < cell.y].index(True)

        # mat = [self.LEFT, self.RIGHT, self.TOP, self.BOTTOM]
        # for arr in mat:
        #     for i, elem in enumerate(arr[::-1]):
        #         if elem.state == -1:
        #             del arr[-i:]

        WithinRange = False
        [elem.state for elem in self.left].index(-1)
        if cell.state == -1:
            mat = [self.LEFT[self.x - cell.x:], self.RIGHT[cell.x - self.x:], self.TOP[self.y - cell.y:], self.BOTTOM[cell.y - self.y:]]
            if mat[index] != []:
                WithinRange = True
                del mat[index]
        elif cell.state == 0:
            mat = [self.LEFT[self.leftVal:self.leftVal + self.freedom], self.RIGHT[self.rightVal:self.freedom], self.TOP[self.topVal:self.freedom], self.BOTTOM[self.bottomVal:self.freedom]]
            for count, elem in enumerate(mat[index]):
                if elem.state < 0:
                    break
            if count:
                WithinRange = True
                self.freedom -= count
                # match index:
                #     case 0:
                #         self.leftVal += count
                #     case 1:
                #         self.rightVal += count
                #     case 2: 
                #         self.topVal += count
                #     case 3: 
                #         self.bottomVal += count
                if index == 0:
                    self.leftVal += count
                elif index == 1:
                    self.rightVal += count
                elif index == 2:
                    self.topVal += count
                elif index == 3:
                    self.bottomVal += count

                # reduce self.LEFT when it oversteps by connecting to a secondary cluster
                # is this unnecessary? let's try without it first. 
                # for arr in [self.LEFT[self.leftVal + self.freedom::-1], self.RIGHT[self.rightVal + self.freedom::-1], 
                #             self.TOP[self.topVal + self.freedom::-1], self.BOTTOM[self.bottomVal + self.freedom::-1]]:
                #     for i, elem in enumerate(arr):
                #         if elem < 0:
                #             del arr[i:]
                #             break

        return index if WithinRange else -1

    # create a direction function which directly passes the index. 
    def predict(self):
        # Each numbered cell has 24 permuations for the order of completing the 4 cardinal directions
        direction = WithinRange()
        # loop this until not WithinRange, or for a better description: no change to freedom or left/right/top/bottom states? 
        if direction != -1:
            # One specific dot is included in all solutions imaginable
            # Only one direction remains for this number to look in
            diff = len(self.LEFT) + len(self.RIGHT) + len(self.TOP) + len(self.BOTTOM) - self.state
            mat = [self.LEFT[self.leftVal:-diff], self.RIGHT[self.rightVal:-diff], self.TOP[self.topVal:-diff], self.BOTTOM[self.bottomVal:-diff]]
            for arr in [self.LEFT[self.leftVal:], self.RIGHT[self.rightVal:-diff], self.TOP[self.topVal:-diff], self.BOTTOM[self.bottomVal:-diff]]:
                for count, elem in enumerate(arr):
                    if elem.state > 0 and count < len(arr) - diff:
                        break
                    elem.markBlue() # does marking blue connect to secondary clusters? prep current cell for if it can see all its dots from connecting to secondary clusters

                self.freedom -= count
                if direction == 0:
                    self.leftVal += count
                    update = self.LEFT[self.leftVal]
                elif direction == 1:
                    self.rightVal += count
                elif direction == 2:
                    self.topVal += count
                elif direction == 3:
                    self.bottomVal += count

            # This number can see all its dots
            # Looking further in one direction would exceed this number
            if sum([elem.state >= 0 for elem in Cell.board[self.leftVal + 1:self.freedom + self.leftVal + 1:-1]]) == self.freedom:
                self.left[self.leftVal].markRed(0)
            if sum([elem.state >= 0 for elem in Cell.board[self.rightVal + 1:self.freedom + self.rightVal  + 1]]) == self.freedom:
                self.left[self.leftVal].markRed(1)
            if sum([elem.state >= 0 for elem in self.TOP[self.topVal + 1:self.freedom + self.topVal + 1]]) == self.freedom:
                self.left[self.leftVal].markRed(2)
            if sum([elem.state >= 0 for elem in self.BOTTOM[self.bottomVal + 1:self.freedom + self.bottomVal + 1]]) == self.freedom:
                self.left[self.leftVal].markRed(3)

            Cell.predictions.discard(self)