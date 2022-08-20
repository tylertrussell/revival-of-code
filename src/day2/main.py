import os


INPUT_FILE = 'input.txt'


def get_input():
  fname = os.path.join(
    os.path.dirname(__file__),
    INPUT_FILE,
  )
  with open(fname, 'r') as f:
    lines = f.read().splitlines()
  return [
    map(int, line.split('x'))
    for line in lines
    if line
  ]


def get_side_permutations(l, w, h):
  return [(l, w), (w, h), (l, h)]


def _get_surface_area(l, w, h):
  return 2 * sum(
    x * y
    for (x, y)
    in get_side_permutations(l, w, h)
  )


def _get_smallest_side(l, w, h):
  return min([
    x * y
    for x, y in get_side_permutations(l, w, h)
  ])


def _get_shortest_perimeter(l, w, h):
  return min([
    2 * (x + y)
    for x, y in get_side_permutations(l, w, h)
  ])


def _calculate_cubic_volume(l, w, h):
  return l * w * h


def calculate_package_paper(l, w, h):
  surface_area = _get_surface_area(l, w, h)
  smallest_side = _get_smallest_side(l, w, h)
  return surface_area + smallest_side


def calculate_ribbon(l, w, h):
  ribbon_feet = _get_shortest_perimeter(l, w, h)
  bow_feet = _calculate_cubic_volume(l, w, h)
  return ribbon_feet + bow_feet


def solve_puzzle_part_one():
  input_data = get_input()
  sqft = 0
  for l, w, h in input_data:
    sqft += calculate_package_paper(l, w, h)
  return sqft


def solve_puzzle_part_two():
  input_data = get_input()
  feet = 0
  for l, w, h in input_data:
    feet += calculate_ribbon(l, w, h)
  return feet


print(f'{solve_puzzle_part_one()}')
print(f'{solve_puzzle_part_two()}')
