import os
from collections import defaultdict

from lib.file_util import get_file_path, get_raw_file


INPUT_FILE = 'input.txt'

DELTAS = {
  '>': (1, 0),
  '<': (-1, 0),
  '^': (0, 1),
  'v': (0, -1)
}


def add(coord_tuple, delta_tuple):
  x, y = coord_tuple
  dx, dy = delta_tuple
  return (x + dx, y + dy)


def get_input():
  fname = get_file_path(__file__, INPUT_FILE)
  return get_raw_file(fname)


def solve_puzzle_part_one():
  presents_count = defaultdict(int)  # tuple: int
  coords = (0, 0)
  input_str = get_input()
  for c in get_input():
    presents_count[coords] += 1
    coords = add(coords, DELTAS[c])
  return len(presents_count.keys())


def solve_puzzle_part_two():
  presents_count = defaultdict(int)  # tuple: int
  coords = {
    1: (0, 0),  # santa
    -1: (0, 0),  # robo-santa
  }
  presents_count[(0, 0)] = 2
  player = 1
  for c in get_input():
    t_coords = coords[player]
    t_coords = add(t_coords, DELTAS[c])
    presents_count[t_coords] += 1
    coords[player] = t_coords
    player *= -1
  return len(presents_count.keys())


if __name__ == '__main__':
  print(f'puzzle 1: {solve_puzzle_part_one()}')
  print(f'puzzle 2: {solve_puzzle_part_two()}')
