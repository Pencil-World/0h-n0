class Cell:
    def __init__(self, x, y, state = None):
        self.x = x
        self.y = y
        self.state = state
  
    def __str__(self):
        return self.state

    