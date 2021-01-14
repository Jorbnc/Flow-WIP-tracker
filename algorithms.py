def search(L, e):
    """ Guttag's Binary Search.
    Assumes L is a list, the elements of which are in
    ascending order.
    Returns True if e is in L and False otherwise"""

    def bSearch(L, e, low, high):
        # Decrements high - low
        if high == low:
            return L[low] == e
        mid = (low + high) // 2
        if L[mid] == e:
            return True
        elif L[mid] > e:
            if low == mid:  # nothing left to search
                return False
            else:
                return bSearch(L, e, low, mid - 1)
        else:
            return bSearch(L, e, mid + 1, high)

    if len(L) == 0:
        return False
    else:
        return bSearch(L, e, 0, len(L) - 1)


def dynamic_count(e, L, start):
    counter = 0
    for i in range(start, len(L)):
        if L[i] == e:
            counter += 1
            start += 1
        else:
            break
    return counter
