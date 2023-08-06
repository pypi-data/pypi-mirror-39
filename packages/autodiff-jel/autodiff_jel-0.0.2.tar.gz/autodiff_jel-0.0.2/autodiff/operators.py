import numpy as np
from .node import Node
from .node import node_decorate

class Log(Node):
  def __init__(self):
    super().__init__()
    self.type = "Log"

  @node_decorate('evaluate')
  def eval(self, values):
    value, base = values
    return np.log(value) / np.log(base)

  @node_decorate('differentiate')
  def diff(self, values, diffs):
    node_value, base_value = values
    node_diff, base_diff = diffs
    g = np.log(node_value)
    g_prime = (node_diff / node_value)
    h = np.log(base_value)
    h_prime = (base_diff / base_value)
    return (g_prime * h - g * h_prime) / (h ** 2)

def log(node, base=np.e):
  return Node.make_node(Log(), node, base)

class Exp(Node):
  def __init__(self):
    super().__init__()
    self.type = "Exponential"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.exp(values[0])

  @node_decorate('differentiate')
  def diff(self, values, diffs):
    return np.exp(values[0]) * diffs[0]

def exp(node):
  return Node.make_node(Exp(), node)

class Sqrt(Node):
  def __init__(self):
    super().__init__()
    self.type = "Squared Root"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.sqrt(values[0])

  @node_decorate('differentiate')
  def diff(self, values, diffs):
    return 1/(2 * values[0]) * diffs[0]

def sqrt(node):
  return Node.make_node(Sqrt(), node)

class Sin(Node):
  def __init__(self):
    super().__init__()
    self.type = "Sine"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.sin(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    return np.cos(value[0]) * diffs[0]

def sin(node):
  return Node.make_node(Sin(), node)

class Cos(Node):
  def __init__(self):
    super().__init__()
    self.type = "Cosine"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.cos(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    return -np.sin(value[0]) * diffs[0]

def cos(node):
  return Node.make_node(Cos(), node)