from event import Event

class EventQueue:

    def __init__(self):
        self.queue = []

    def peek():
        if len(self.queue) > 0:
            return self.queue[0]

    def pop():
        if len(self.queue) <= 0:
            return None
        return self.queue.pop(0)
    
    def add(self, item):
        self.queue.append(item)
        self.sort(0,len(self.queue)-1)
    
    def sort(self, lo, hi):
        i = lo
        j = hi
        # calculate pivot number, I am taking pivot as middle index number
        pivot = self.queue[int(lo+(hi-lo)/2)]
        # Divide into two arrays
        while i <= j:
            
            # In each iteration, we will identify a number from left side which
            # is greater then the pivot value, and also we will identify a number
            # from right side which is less then the pivot value. Once the search
            # is done, then we exchange both numbers.
            
            while self.queue[i].eventTime < pivot.eventTime:
                i += 1
            
            while self.queue[j].eventTime > pivot.eventTime:
                j -= 1
            
            if i <= j:
                self.swap(i, j)
                #move index to next position on both sides
                i+=1
                j-=1

        #call quickSort() method recursively
        if lo < j:
            self.sort(lo, j)
        if i < hi:
            self.sort(i, hi)

    def swap(self, i, j):
        tmp = self.queue[i]
        self.queue[i] = self.queue[j]
        self.queue[j] = tmp

    def print(self):
        for i in range(len(self.queue)):
            print(str(self.queue[i].eid) + " " + str(self.queue[i].eventTime)  + " " + str(self.queue[i].type))