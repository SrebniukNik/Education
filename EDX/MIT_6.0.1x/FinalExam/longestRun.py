def longestRun(L):
  count = 1
  longest = []
  for idx in range(len(L)-1):
    if L[idx] <= L[idx+1]:
      count += 1
    else:
      longest.append(count)
      count = 1
  longest.append(count)
  return max(longest)

print longestRun([0])

print longestRun([10, 4, 6, 8, 3, 4, 5, 7, 7, 2])

print longestRun([1, 1, 1, 1, 1])

print longestRun([-10, -5, 0, 5, 10])