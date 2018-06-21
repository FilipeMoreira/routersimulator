

class Queue:

    def __init__(self):
        self.queue = []

    def add(self, item):
        self.queue.append(item)

    def peek(self):
        if len(self.queue) < 1:
            return None
        return self.queue[0]
    
    def pop(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    