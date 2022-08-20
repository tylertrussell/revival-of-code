from collections import defaultdict
import re

from lib.file_util import get_file_path, get_input_as_lines


NAUGHTY_STRINGS = ['ab', 'cd', 'pq', 'xy']


INPUT_FILE = 'input.txt'
def get_input():
  fname = get_file_path(__file__, INPUT_FILE)
  return get_input_as_lines(fname)


def isnice(s):
  vowel_count = 0
  last_letter = None
  found_double = False
  if any([x in s for x in NAUGHTY_STRINGS]):
    return False
  for c in s:
    if c in {'a', 'e', 'i', 'o', 'u'}:
      vowel_count += 1
    if last_letter == c:
      found_double = True
    if vowel_count >= 3 and found_double:
      return True
    last_letter = c


def isnice_v2(s):
  criteria = [r'.*(\w\w).*\1.*', r'.*(.).\1.*']
  for criterion in criteria:
    if re.fullmatch(criterion, s) is None:
      return False
  return True


def solve_puzzle_part_one():
  nice_lines = [
    line for line in get_input()
    if isnice(line)
  ]
  return len(nice_lines)


def solve_puzzle_part_two():
  nice_lines = [
    line for line in get_input()
    if isnice_v2(line)
  ]
  return len(nice_lines)


if __name__ == '__main__':
  print(f'part 1: {solve_puzzle_part_one()}')
  print(f'part 2: {solve_puzzle_part_two()}')
