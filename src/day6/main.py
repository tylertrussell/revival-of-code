from collections import defaultdict
import re

from lib.file_util import get_file_path, get_input_as_lines


INPUT_FILE = 'input.txt'
def get_input():
  fname = get_file_path(__file__, INPUT_FILE)
  return get_input_as_lines(fname)


def create_light_grid():
  return [
    [0 for i in range(1000)]
    for i in range(1000)
  ]


def parse_instructions(instruction_str):
  regex = r'(turn on|turn off|toggle) (\d{1,3},\d{1,3}) through (\d{1,3},\d{1,3})'
  match = re.match(regex, instruction_str)
  return match.groups()  # action, start, end


def solve_puzzle_part_one():
  lights = create_light_grid()
  for line in get_input():
    action, start, end = parse_instructions(line)
    x1, y1 = map(int, start.split(','))
    x2, y2 = map(int, end.split(','))
    for x in range (x1, x2 + 1):
      for y in range(y1, y2 + 1):
        if action == 'turn on':
          lights[x][y] = 1
        elif action == 'turn off':
          lights[x][y] = 0
        elif action == 'toggle':
          current_val = lights[x][y]
          lights[x][y] = 0 if current_val == 1 else 0
  return sum([ sum(row) for row in lights ])


def solve_puzzle_part_two():
  lights = create_light_grid()
  for line in get_input():
    action, start, end = parse_instructions(line)
    x1, y1 = map(int, start.split(','))
    x2, y2 = map(int, end.split(','))
    for x in range (x1, x2 + 1):
      for y in range(y1, y2 + 1):
        current_val = lights[x][y]
        if action == 'turn on':
          lights[x][y] += 1
        elif action == 'turn off':
          lights[x][y] = max(current_val - 1, 0)
        elif action == 'toggle':
          lights[x][y] += 2
  return sum([ sum(row) for row in lights ])

if __name__ == '__main__':
  print(f'Part 1: {solve_puzzle_part_one()}')
  print(f'Part 2: {solve_puzzle_part_two()}')

