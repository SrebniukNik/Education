def stdDevOfLengths(L):
  """
  L: a list of strings

  returns: float, the standard deviation of the lengths of the strings,
    or NaN if L is empty.
  """
  if not L:
    return float('NaN')
  else:
    mean = sum(len(s) for s in L) / float(len(L))
    sm = []
    for i in range(len(L)):
      sm.append((len(L[i]) - mean) ** 2)
    return (sum(sm) / len(L)) ** 0.5

#print stdDevOfLengths(['a', 'z', 'p'])

#print stdDevOfLengths(['apples', 'oranges', 'kiwis', 'pineapples'])


def stdDevOfLengths(L):
  """
  L: a list of strings

  returns: float, the standard deviation of the lengths of the strings,
    or NaN if L is empty.
  """
  if not L:
    return float('NaN')
  else:
    mean = sum(L) / float(len(L))
    sm = []
    for i in range(len(L)):
      sm.append((L[i] - mean) ** 2)
    return (sum(sm) / len(L)) ** 0.5 / mean

print stdDevOfLengths([1,2,3])

print stdDevOfLengths([11,12,13])


