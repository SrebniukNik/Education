def gen_all_strings(word):
  """
  Generate all strings that can be composed from the letters in word
  in any order.

  Returns a list of all strings that can be formed from the letters
  in word.

  This function should be recursive.
  """
  if not word:
    return ['']
  all_variants = []
  for letters in gen_all_strings(word[1:]):
    print letters
    for index in range(len(letters) + 1):
      all_variants.append(letters[:index] + word[0] + letters[index:])
  return gen_all_strings(word[1:]) + all_variants

print gen_all_strings('acvbd')