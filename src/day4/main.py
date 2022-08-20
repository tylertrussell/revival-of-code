import hashlib

INPUT = 'iwrupvqb{}'


def solve_puzzle_one():
  i = 0
  while True:
    s = INPUT.format(i)
    this_hash = hashlib.md5(s.encode())
    if this_hash.hexdigest().startswith('000000'):
      return i
    i += 1
    if i % 1000 == 0:
      print(i)


if __name__ == '__main__':
  print(f'Solve 1: {solve_puzzle_one()}')
