# sort.py
def merge_sort(arr, key=None):
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)

def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_val = left[i] if key is None else key(left[i])
        right_val = right[j] if key is None else key(right[j])
        if left_val <= right_val:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result