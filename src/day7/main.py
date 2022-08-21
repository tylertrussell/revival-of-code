import re
import uuid

from lib.file_util import get_input_as_lines, get_file_path

"""
as RSHIFT 3 -> au
cz OR cy -> da
NOT cv -> cw
14146 -> b
"""

class Network(object):

  singleton = None
  @classmethod
  def get_network(cls):
    if not cls.singleton:
      cls.singleton = Network()
    return cls.singleton

  def __init__(self):
    self.network = {}
    self.cached = {}

  def add_node(self, node):
    self.network[node.name] = node

  def get_value(self, name):
    if name in self.cached:
      return self.cached[name]
    calculated = self.network[name].get_value()
    self.cached[name] = calculated
    return calculated


class Wire(object):
  def __init__(self, name, value):
    if name == 'e':
      import pudb
      pudb.set_trace()
    self.name = name
    self.value = value

  def get_value(self):
    if isinstance(self.value, int):
      # print(f'{self.name} is {self.value}')
      return self.value
    if isinstance(self.value, str):
      if self.value == 'e':
        import pudb
        pudb.set_trace()
      net = Network.get_network()
      value = net.get_value(self.value)
      # print(f'{self.value} value is {value}')
      return value

  def __str__(self):
    return str(self.get_value())


class Gate(object):
  def __init__(self, name, gate_type, input1, input2):
    assert gate_type in ('AND', 'OR', 'LSHIFT', 'RSHIFT')
    self.name = name
    self.gate_type = gate_type
    self.input1 = input1
    self.input2 = input2

  def _resolve_value(self, input_name):
    net = Network.get_network()
    if input_name.isnumeric():
      return int(input_name)
    else:
      value = net.get_value(input_name)
      # print(f'{input_name} value is {value}')
      return value

  def get_value(self):
    # print(f'{self.name} is {self.input1} {self.gate_type} {self.input2}')
    val1 = self._resolve_value(self.input1)
    val2 = self._resolve_value(self.input2)
    if self.gate_type == 'AND':
      result = val1 & val2
    elif self.gate_type == 'OR':
      result = val1 | val2
    elif self.gate_type == 'LSHIFT':
      result = val1 << val2
    elif self.gate_type == 'RSHIFT':
      result = val1 >> val2
    return result
    # print(f'{self.input1} {self.gate_type} {self.input2} = {result}')

  def __str__(self):
    return str(self.get_value())


class Not(object):
  def __init__(self, name, input1):
    self.name = name
    self.input1 = input1

  def get_value(self):
    # print(f'computing NOT gate for {self.input1}')
    net = Network.get_network()
    val1 = net.get_value(self.input1)
    return val1 ^ 0xffff

  def __str__(self):
    return str(self.get_value())


def split_expression(expression):
  """
  Args:
    expression: (lside) -> (rside)
  Returns:
    lside, rside (strings)
  """
  split_re = r'(.*) -> (\w+)'
  return re.match(split_re, expression).groups()


def split_left_logical(expression):
  """
  Args:
    expression: left side logical expression e.g.
      as RSHIFT 3 -> au
      cz OR cy -> da
  Returns:
    var1, op, var2|value
  """
  logical_re = r'(\w+) (AND|OR|RSHIFT|LSHIFT) (\d+|\w+)?'
  match = re.match(logical_re, expression)
  if match:
    return match.groups()


def is_not_expression(expression):
  """
  Args:
    expression: e.g. NOT abc
  Returns:
    negated variable name or None
  """
  not_re = r'NOT (\w+)'
  match = re.match(not_re, expression)
  if match:
    return match.groups()[0]


def is_const_expression(expression):
  """
  Args:
    expression: e.g. 1234
  Returns:
    int or None
  """
  const_re = '(\d+|\w+)'
  match = re.match(const_re, expression)
  if match:
    val = match.groups()[0]
    if val.isnumeric():
      return int(val)
    return val


def eval_expression(expression):
  """
  Returns:
    True if the expression evaluated successfully
    False if the expression could not be evaluated, e.g.:
      if the variables have no values yet
  """
  network = Network.get_network()

  left, name = split_expression(expression)

  left_side = split_left_logical(left)
  if left_side:
    var1, op, var2 = left_side
    network.add_node(Gate(name, op, var1, var2))
    return True

  negated_var = is_not_expression(left)
  if negated_var:
    network.add_node(Not(name, negated_var))
    return True

  # being a very broad regex, const must come last
  const = is_const_expression(left)
  if const is not None:
    network.add_node(Wire(name, const))
    return True


def get_input():
  return get_input_as_lines(
    get_file_path(__file__, 'input.txt')
  )


if __name__ == '__main__':
  lines = get_input()

  for line in lines:
    success = eval_expression(line)
    assert success, f'{line} failed to eval'

  a = Network.get_network().get_value('a')
  print(f'value for a is: {a}')

  eval_expression(f'{a} -> b')
  Network.get_network().cached = {}
  a = Network.get_network().get_value('a')
  print(f'new value for a is: {a}')
