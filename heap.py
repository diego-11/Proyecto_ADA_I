# heap.py
class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, distancia, fila, columna):
        self.heap.append((distancia, fila, columna))
        self._sift_up(len(self.heap)-1)
    
    def _sift_up(self, idx):
        parent = (idx-1)//2
        if parent >= 0 and self.heap[parent][0] > self.heap[idx][0]:
            self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
            self._sift_up(parent)
    
    def pop(self):
        if not self.heap:
            return None
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item = self.heap.pop()
        self._sift_down(0)
        return item
    
    def _sift_down(self, idx):
        smallest = idx
        left = 2*idx+1
        right = 2*idx+2
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._sift_down(smallest)
    
    def size(self):
        return len(self.heap)
    
    def is_empty(self):
        return len(self.heap) == 0