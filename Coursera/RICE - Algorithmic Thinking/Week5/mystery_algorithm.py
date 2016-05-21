def mystery(lists, l, r):
    if l > r:
        return -1
    m = (l + r) / 2
    if lists[m] == m:
        return m
    else:
        if lists[m] < m:
            return mystery(lists, m + 1, r)
        else:
            return mystery(lists, l, m - 1)

print mystery([-2,0,1,3,7,12,15],0,6)