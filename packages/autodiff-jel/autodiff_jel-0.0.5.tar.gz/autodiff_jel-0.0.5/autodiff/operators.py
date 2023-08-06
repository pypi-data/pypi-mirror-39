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

    # Ignores zero errors:
    # node_value, base_value = [np.array(val,dtype=float) for val in values]
    # node_diff, base_diff = [np.array(val,dtype=float) for val in diffs]

    g = np.log(node_value)
    g_prime = (node_diff / node_value)
    h = np.log(base_value)
    h_prime = (base_diff / base_value)

    # Ignores zero errors:
    # g = np.log(node_value, out=np.zeros_like(node_value), where=node_value!=0)
    # g_prime = np.divide(node_diff, node_value, out=np.zeros_like(node_diff), where=node_value!=0)
    # h = np.log(base_value, out=np.zeros_like(base_value), where=base_value!=0)
    # h_prime = np.divide(base_diff, base_value, out=np.zeros_like(base_diff), where=base_value!=0)


    return (g_prime * h - g * h_prime) / (h ** 2)

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    val, base = values
    val_out = np.divide(grad_value, np.multiply(np.log(base), val))
    base_1 = np.power(np.divide(np.log(val), np.log(base)),2)
    base_2 = np.multiply(val, np.log(base))
    base_out = np.divide(-grad_value, np.multiply(base_1, base_2))

    return (val_out, base_out)

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

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
   	return (np.multiply(np.exp(values[0]), grad_value),)

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
    return 1/(2 * np.sqrt(values[0])) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
   	return (np.divide(grad_value, 2*np.sqrt(values[0])),)

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

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
   	return (np.multiply(grad_value, np.cos(values[0])),)

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

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
   	return (np.multiply(-grad_value, np.sin(values[0])),)

def cos(node):
  return Node.make_node(Cos(), node)

class Tan(Node):
  def __init__(self):
    super().__init__()
    self.type = "Tangent"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.tan(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.cos(value[0])
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return (np.divide(1, denom)**2) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.cos(values[0])
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return (np.multiply((np.divide(1, denom)**2), grad_value),)

def tan(node):
  return Node.make_node(Tan(), node)

class Arcsin(Node):
  def __init__(self):
    super().__init__()
    self.type = "Arcsin"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.arcsin(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.sqrt(np.subtract(1, value[0]**2))
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return np.divide(1, denom) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.sqrt(np.subtract(1, values[0]**2))
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return (np.multiply(np.divide(1, denom), grad_value),)

def arcsin(node):
  return Node.make_node(Arcsin(), node)

class Arccos(Node):
  def __init__(self):
    super().__init__()
    self.type = "Arccos"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.arccos(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.sqrt(np.subtract(1, value[0]**2))
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return -np.divide(1, denom) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.sqrt(np.subtract(1, values[0]**2))
    if np.any(np.round(denom, 4) == 0.0000):
      raise ZeroDivisionError('Division by zero.')
    return (np.multiply(-np.divide(1, denom), grad_value),)

def arccos(node):
  return Node.make_node(Arccos(), node)

class Arctan(Node):
  def __init__(self):
    super().__init__()
    self.type = "Arctan"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.arctan(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.add(value[0]**2, 1)
    return np.divide(1, denom) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.add(values[0]**2, 1)
    return (np.multiply(np.divide(1, denom), grad_value),)

def arctan(node):
  return Node.make_node(Arctan(), node)

class Sinh(Node):
  def __init__(self):
    super().__init__()
    self.type = "Sinh"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.sinh(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    return np.cosh(value[0]) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
  	return (np.multiply(np.cosh(values[0]), grad_value),)

def sinh(node):
  return Node.make_node(Sinh(), node)

class Cosh(Node):
  def __init__(self):
    super().__init__()
    self.type = "Cosh"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.cosh(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    return np.sinh(value[0]) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
  	return (np.multiply(np.sinh(values[0]), grad_value),)

def cosh(node):
  return Node.make_node(Cosh(), node)

class Tanh(Node):
  def __init__(self):
    super().__init__()
    self.type = "Tanh"

  @node_decorate('evaluate')
  def eval(self, values):
    return np.tanh(values[0])

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.cosh(value[0])
    return (np.divide(1, denom)**2) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.cosh(values[0])
    return (np.multiply((np.divide(1, denom)**2), grad_value),)

def tanh(node):
  return Node.make_node(Tanh(), node)

class Logistic(Node):
  def __init__(self):
    super().__init__()
    self.type = "Logistic"

  @node_decorate('evaluate')
  def eval(self, values):
    denom = np.add(1, np.exp(-values[0]))
    return np.divide(1, denom)

  @node_decorate('differentiate')
  def diff(self, value, diffs):
    denom = np.power(np.add(1, np.exp(-value[0])), 2)
    return np.divide(np.exp(-value[0]), denom) * diffs[0]

  @node_decorate('reverse')
  def reverse(self, values, grad_value):
    denom = np.power(np.add(1, np.exp(-values[0])), 2)
    return (np.multiply(np.divide(np.exp(-values[0]), denom), grad_value),)

def logistic(node):
  return Node.make_node(Logistic(), node)