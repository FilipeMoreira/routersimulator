#encoding: utf-8
from event import Event

class EventQueue:

    def __init__(self):
        self.queue = []

    def peek(self):
        if len(self.queue) > 0:
            return self.queue[0]

    def pop(self):
        if len(self.queue) <= 0:
            return None
        return self.queue.pop(0)
    
    def add(self, item):
        target_index = 0
        inserted = 0
        for index, evt in enumerate(self.queue):
            if evt.eventTime >= item.eventTime:
                self.queue.insert(index, item)
                inserted = 1
                break
        if inserted == 0:
            self.queue.append(item)
        # self.queue.append(item)
        # self.sort(0,len(self.queue)-1)

    def remove_with_package(self, _package):
        for index, evt in enumerate(self.queue):
            if evt.package_reference == _package:
                del self.queue[index]
                break

    def get(self, index):
        return self.queue[index]
    
    def length(self):
        return len(self.queue)

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

    def printQueue(self):
        print('---')
        for i in range(len(self.queue)):
            print(str(self.queue[i].eventTime)  + " " + str(self.queue[i].type))
            
        print('---')