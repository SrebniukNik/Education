def remove_duplicates(list1):
  """
  Eliminate duplicates in a sorted list.

  Returns a new sorted list with the same elements in list1, but
  with no duplicates.

  This function can be iterative.
  """
  if not list1 or len(list1) <= 1:
    return list1
  firstval = list1[0]
  while firstval in list1:
    list1.remove(firstval)
  return [firstval] + remove_duplicates(list1)

#print remove_duplicates([1,2,3,4,2,3,4])

def intersect(list1, list2):
  """
  Compute the intersection of two sorted lists.

  Returns a new sorted list containing only elements that are in
  both list1 and list2.

  This function can be iterative.
  """
  if len(list1) < len(list2):
      list1, list2 = list2, list1
  intersected_list = []
  for item in list1:
    if item in list2:
      intersected_list.append(item)
  return intersected_list

print intersect([1,2,3,4],[2,3,4])


def quicksort(num_list):
  """
  Recursive O(n log(n)) sorting algorithm
  Takes a list of numbers
  Returns sorted list of same numbers
  """
  if not num_list:
    return num_list
  else:
    pivot = num_list[0]
    lesser = [num for num in num_list if num < pivot]
    pivots = [num for num in num_list if num == pivot]
    greater = [num for num in num_list if num > pivot]
    return quicksort(lesser) + pivots + quicksort(greater)


def merge(list1, list2):
  """
  Merge two sorted lists.

  Returns a new sorted list containing those elements that are in
  either list1 or list2.

  This function can be iterative.
  """
  if list2:
    list1.extend(list2)

  return remove_duplicates(quicksort(list1))

#print merge([1,2,3,4],[2,3,4,6,6,6,8,7,5,0])


def merge_sort(list1):
  """
  Sort the elements of list1.

  Return a new sorted list with the same elements as list1.

  This function should be recursive.
  """
  if len(list1) < 2:
    return list1[:]
  if len(list1) > 1:
    middle = len(list1) / 2
    sublist1 = merge_sort(list1[:middle])
    sublist2 = merge_sort(list1[middle:])
    return  merge(sublist1, sublist2)


print merge_sort([1,2,3,4,2,3,4,6,6,6,8,7,5,0])