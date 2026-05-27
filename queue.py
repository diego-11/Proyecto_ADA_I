# queue.py
class Queue:
    def __init__(self):
        self.items = []
        self.front = 0
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if self.front >= len(self.items):
            return None
        item = self.items[self.front]
        self.front += 1
        return item
    
    def is_empty(self):
        return self.front >= len(self.items)
    
    def size(self):
        return len(self.items) - self.front