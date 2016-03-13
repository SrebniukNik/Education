def genPrimes():
    prime_list = []
    prime_cand = 1
    while True:
      prime_cand += 1
      for prime in prime_list:
        if prime_cand % prime == 0:
          break
      else:
        prime_list.append(prime_cand)
        yield prime_cand

for n in genPrimes():
  print n