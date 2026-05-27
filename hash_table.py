# hash_table.py
class HashTable:
    def __init__(self, capacity=100003, hash_func=None):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]
        self.hash_func = hash_func if hash_func else self._default_hash
    
    def _default_hash(self, key):
        # Para claves que sean tuplas o enteros o strings
        if isinstance(key, tuple):
            # Combinación de dos enteros: fila, columna
            return (key[0] * 1000003 + key[1]) % self.capacity
        elif isinstance(key, str):
            # hash simple para strings
            h = 0
            for ch in key:
                h = (h * 31 + ord(ch)) % self.capacity
            return h
        else:
            return hash(key) % self.capacity
    
    def put(self, key, value):
        idx = self.hash_func(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
    
    def get(self, key):
        idx = self.hash_func(key)
        for k, v in self.table[idx]:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        idx = self.hash_func(key)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False
    
    def items(self):
        for bucket in self.table:
            for k, v in bucket:
                yield (k, v)
    
    def keys(self):
        for bucket in self.table:
            for k, v in bucket:
                yield k
    
    def __contains__(self, key):
        return self.get(key) is not None