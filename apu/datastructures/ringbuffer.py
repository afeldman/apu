from collections import deque

class CircularBuffer(deque):
    def __init__(self, size=1):
        super().__init__(maxlen=size)

    @property
    def average(self):
        if not isinstance(self, int) or not isinstance(self, float):
            raise TypeError ("check if int or float")

        return sum(self)/len(self)
