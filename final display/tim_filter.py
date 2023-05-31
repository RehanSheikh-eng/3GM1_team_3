class MovingAverage:

    def __init__(self, depth):
        depth = int(depth)

        self.values = [0.0] * depth
        
    def update(self, value):
        self.values.insert(0, value)
        self.values.pop()

        return sum(self.values) / len(self.values)