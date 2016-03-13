def dict_invert(d):
  '''
  d: dict
  Returns an inverted dictionary according to the instructions above
  '''
  list_of_dict = [[v, k] for k, v in d.iteritems()]
  list_of_dict.sort(key=lambda l: l[1])
  final = {}
  for k in list_of_dict:
    if k[0] in final.keys():
      final[k[0]].append(k[1])
    else:
      final[k[0]] = [k[1]]

  return final


dict_invert({1:10, 2:20, 3:10, 0:15})

