def getSublists(L, n):
  new_list = []
  for idx in range(0, len(L)-n+1):
    new_list += [L[idx:idx+n]]
  print new_list

print getSublists([10, 4, 6, 8, 3, 4, 5, 7, 7, 2],4)