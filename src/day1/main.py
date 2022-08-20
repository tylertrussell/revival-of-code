from collections import Counter
import os

INPUT_FILENAME = 'input.txt'


def get_input():
  fname = os.path.join(
    os.path.dirname(__file__),
    INPUT_FILENAME,
  )
  with open(fname, 'r') as f:
    return f.read().strip()


def solve_puzzle_part_1():
  input_data = get_input()
  counter = Counter(input_data)
  assert set(counter.keys()) == {'(', ')'}
  
  return counter['('] - counter[')']


def solve_puzzle_part_2():
  input_data = get_input()
  current_floor = 0
  cmds = {'(': 1, ')': -1}
  for idx, cmd in enumerate(input_data):
    current_floor += cmds[cmd]
    if current_floor == -1:
      return idx + 1  # per instructions, index 1-based


print(f'part 1: {solve_puzzle_part_1()}')

print(f'part 2: {solve_puzzle_part_2()}')

