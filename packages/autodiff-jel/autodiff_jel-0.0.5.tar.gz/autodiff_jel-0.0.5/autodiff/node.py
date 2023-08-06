""" 
Node Logic for Automatic Differentiation
"""

from functools import wraps
import numpy as np
import numbers
from .visualization import create_computational_graph, create_computational_table
from .settings import settings

"""
Custom exceptions. 
"""
class NoValueError(Exception):
	pass

class node_decorate():
		""" Decorator for computation functions.

		Implemented as a class for clarity and to serve
		as a decorator factory.

		Note: the class implementation of decorators behaves
		very differently in the case the decorator pattern takes
		arguments (__call__ is called only once at decoration,
		since we have another function layer outside now).
		"""

		def __init__(self, mode):
		  # Maintain function metadata (doctstrings, etc.) with wraps
			self.factory = {'evaluate': self.eval_wrapper,
							'differentiate': self.diff_wrapper,
							'reverse': self.reverse_wrapper}
			self.wrapper = self.factory[mode]

		def __call__(self, fn):

			return self.wrapper(fn)

		def eval_wrapper(self, fn):
			""" Wrapper for updating node values. """
			@wraps(fn)
			def wrapper(self):
				values = [child.eval() for child in self.children]
				result = fn(self, values)
				self.set_value(result)
				return result
			return wrapper

		def diff_wrapper(self, fn):
			""" Wrapper for updating node derivatives. """
			@wraps(fn)
			def wrapper(self):
				values = [child.eval() for child in self.children]
				diffs = [child.diff() for child in self.children]
				result = fn(self, values, diffs)
				self.set_derivative(result)
				return result
			return wrapper

		def reverse_wrapper(self, fn):
			""" Wrapper for updating gradients in reverse pass. """
			@wraps(fn)
			def wrapper(self):
				# Check that we've received all the dependencies we need
				if not self.ready_to_reverse():
					return

				# We need to have done first sweep before reverse, assume values exist
				values = [child.value() for child in self.children]
				grad_value = self._grad_value
				results = fn(self, values, grad_value)

				# Need to propagate results (functions need to return same # of results as children)

				for idx in range(len(results)):
					self.children[idx].add_grad_contribution(results[idx])
					self.children[idx].reverse()

				return results
			return wrapper

class Node():
	""" Class Node

	Base Node implementation.
	"""

	def __init__(self):
		self._value = None
		self._derivative = {}
		self._variables = {}
		self._cur_var = None
		self.children = []

		# Name of type of node
		self.type = 'None'

		# Reverse mode
		self._grad_value = 0
		self._cur_grad_count = 0
		self._grad_count = 0

	@classmethod
	def make_constant(cls, value):
		return Constant(value)

	@classmethod
	def make_node(cls, node, *values):
		new_nodes = []
		for value in values:
			new = value
			if not isinstance(new, Node):
				new = cls.make_constant(value)
			new_nodes.append(new)
		node.set_children(*new_nodes)
		node.update_variables()
		return node


	""" MAGIC

	Various implementations to improve the interface
	of the package, from calling nodes directly to compute
	to treating them as one would expect in symbolic computation.
	"""

	def __call__(self, *args, **kwargs):
		return self.compute(*args, **kwargs)

	def __repr__(self):
		output = 'Node(Function = %r, Value = %r, Derivative = %r)' % (self.type, self.value(), self.derivative())
		return output

	def __add__(self, value):
		node = self.make_node(Addition(), self, value)
		return node

	def __radd__(self, value):
		node = self.make_node(Addition(), value, self)
		return node

	def __neg__(self):
		node = self.make_node(Negation(), self)
		return node

	def __sub__(self, value):
		node = self.make_node(Subtraction(), self, value)
		return node

	def __rsub__(self, value):
		node = self.make_node(Subtraction(), value, self)
		return node

	def __mul__(self, value):
		node = self.make_node(Multiplication(), self, value)
		return node

	def __rmul__(self, value):
		node = self.make_node(Multiplication(), value, self)
		return node

	def __truediv__(self, value):
		node = self.make_node(Division(), self, value)
		return node

	def __rtruediv__(self, value):
		node = self.make_node(Division(), value, self)
		return node

	def __pow__(self, value):
		node = self.make_node(Power(), self, value)
		return node

	def __rpow__(self, value):
		node = self.make_node(Power(), value, self)
		return node

	def __eq__(self,other):
		return self.value() == other.value() and self.derivative() == other.derivative()

	def __ne__(self, other):
		return not self == other

	def __hash__(self):
		return id(self)

	""" ATTRIBUTES

	Methods for setting and getting attributes.
	"""

	def value(self):
		return self._value

	def derivative(self):
		return self._derivative

	def set_value(self, value):
		if not isinstance(value, (numbers.Number, np.ndarray)):
			raise TypeError('Value must be numeric or a numpy array.')
		self._value = value

	def set_derivative(self, value):
		var = self.update_cur_var()
		if isinstance(value, numbers.Number):
			self._derivative[self._cur_var] = value
		else:
			# if self._cur_var not in self._derivative:
			# 	self._derivative[self._cur_var] = np.zeros(value.size)
			self._derivative[self._cur_var][var.var_idx] = value[var.var_idx]

	def set_children(self, *children):
		self.children = children

	""" VARIABLES

	Methods for handling variables, the basic
	stores for actually computing the values and
	derivatives of any given node.
	"""
	def update_variables(self):
		"""	Update current variable list to reflect all variables
		necessary in children.
		"""

		new_vars = []
		for child in self.children:
			if isinstance(child, Variable):
				new_vars.append(child)
			else:
				new_vars.extend(child._variables.values())
		variables = list(set(new_vars))
		variable_names = [var.name for var in variables]
		self._variables = dict(zip(variable_names, variables))

	def set_variables(self, input_dict):
		""" Set variables for evaluation. """

		for key, value in input_dict.items():
			self._variables[key].set_value(value)

			# if isinstance(value, np.ndarray):
			# 	self._derivative[key] = np.zeros(value.size)
		self.zero_vector_derivative(input_dict)

	def zero_vector_derivative(self, input_dict):
		""" Reset vectors of derivatives recursively in children """
		if type(self) != Variable:
			for key, value in input_dict.items():
				if isinstance(value, np.ndarray) and key in self._variables:
					self._derivative[key] = np.zeros(value.size)

			for node in self.children:
				node.zero_vector_derivative(input_dict)

	def update_cur_var(self):
		for v in self._variables:
			if np.any(self._variables[v].derivative()):
				self._cur_var = v
				return self._variables[v]

	def iterate_seeds(self):
		""" Generator to iterate over all variables of this
		node, which assign seed values to variables to compute
		all partials.
		"""

		for var in self._variables:
			# Reset derivatives
			for v in self._variables:
				self._variables[v].set_derivative(0)

			if isinstance(self._variables[var].value(), np.ndarray):
				for idx in self._variables[var].iterate_idxs():
					yield idx
			else:
				self._variables[var].set_derivative(1)
			yield var
	
	""" REVERSE MODE

	Helper functions for properly doing the reverse mode
	of automatic differentiation. These include keeping track
	of whether or not any node is ready to compute its contributions
	to its children, and managing these contributions.
	"""

	def zero_grad_values(self):
		""" Reset all partial contributions for reverse pass """
		self._grad_value = 0
		self._cur_grad_count = 0
		self._grad_count = 0

		for child in self.children:
			child.zero_grad_values()

	def set_grad_count(self):
		""" Calculate dependency counts """
		self._grad_count += 1
		for child in self.children:
			child.set_grad_count()

	def ready_to_reverse(self):
		return (self._cur_grad_count == self._grad_count)

	def add_grad_contribution(self, value):
		# Keep track of addition contribution
		self._cur_grad_count += 1
		self._grad_value += value

	""" COMPUTATION

	 Actual computation functions, with eval and diff
	 to be implemented by subclasses. Use the node_decorate
	 decorator to update node values upon computation.
	"""

	def compute(self, *args, **kwargs):
		""" Evaluate and differentiate at the given variable values.

		Inputs methods:
		-Dictionary of {variable_name: value, ...}
		-Keyword arguments of compute(variable_vame=value, ...)
		"""
		if len(args) == 0:
			input_dict = kwargs
		elif len(args) == 1:
			input_dict = args[0]

		if input_dict.keys() != self._variables.keys():
			raise TypeError('Input not recognized.')

		# Compute the value at this node
		self.set_variables(input_dict)
		self.eval()

		# Compute derivatives based on mode

		if settings.current_mode() == "forward":
			for var in self.iterate_seeds():
				self.diff()
		else: 
			# Reverse mode
			self.zero_grad_values()
			# Get proper contribution counts
			self.set_grad_count()
			# Seeding output, current node by 1
			self.add_grad_contribution(1)
			self.reverse()

			# Now set the results
			self._derivative = {}
			for key, var in self._variables.items():
				self._derivative[key] = var._grad_value

		return self

	# Uncomment when overriding:
	# @node_decorate('evaluate')
	def eval(self, values):
		raise NotImplementedError

	# Uncomment when overriding:
	# @node_decorate('differentiate')
	def diff(self, values, diffs):
		raise NotImplementedError

	# Uncomment when overriding:
	# @node_decorate('reverse')
	def reverse(self, values, grad_value):
		raise NotImplementedError

	def get_comp_graph(self):
		""" Creates a computational graph for a given node. """
		return create_computational_graph(self)

	def get_comp_table(self):
		""" Creates a computational table for a given node. """
		return create_computational_table(self)

""" SUBCLASSES

Node subclasses that define operations or single
values, such as variables and constants.
"""

class Variable(Node):
	"""	Node representing a symbolic variable.

	Serves as the basis of evaluation, and then
	propagates values through the graph
	to the final output values.
	"""

	def __init__(self, name=None):
		super().__init__()
		if name is None or not isinstance(name, str):
			raise ValueError('Name must be given for variable.')
		self.name = name
		self.type = 'Variable'
		self._variables[name] = self
		self.var_idx = -1

	def eval(self):
		if self.value() is None:
			raise NoValueError('Variable %s has been given no value.' % self.name)
		return self.value()

	def diff(self):
		if self.derivative() is None:
			raise NoValueError('Variable %s has been given no value.' % self.name)
		return self.derivative()

	# Override dict functionality for variables; I could keep this
	# consistent, but would increase computation; elegance tradeoff
	def set_derivative(self, value):
		if isinstance(self.value(), np.ndarray):
			self._derivative[:] = value
		else:
			self._derivative = value

	# On value set, needs to set the derivative
	def set_value(self, value):
		self._value = None
		if isinstance(value, np.ndarray):
			self.set_derivative(np.zeros(value.size))
		super().set_value(value)

	# Iterate over each vector position
	def iterate_idxs(self):
		for i in range(self._value.size):
			self.set_derivative(0)
			self.var_idx = i
			self._derivative[i] = 1
			yield i

	# # Override calling the variable
	def compute(self, *args, **kwargs):
		if len(args) == 0:
			input_dict = kwargs
		elif len(args) == 1:
			input_dict = args[0]

		if self.name not in input_dict:
			raise TypeError('Input not recognized.')

		self.set_value(input_dict[self.name])
		self.set_derivative(1);
		return self

	def __call__(self, *args, **kwargs):
		return self.compute(*args, **kwargs)

	# Reverse mode doesn't need to do anything, no children
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		return ()


class Constant(Node):
	""" Node representing a constant.

	Always initiated with 0 derivative.
	"""

	def __init__(self, value):
		super().__init__()
		self.set_value(value)
		self.set_derivative(0)
		self.type = 'Constant'

	def set_derivative(self, value):
		self._derivative = value

	def eval(self):
		return self.value()

	def diff(self):
		return self.derivative()

	# Reverse mode doesn't need to do anything, no children
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		return ()


class Addition(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Addition'

	@node_decorate('evaluate')
	def eval(self, values):
		left, right = values
		return np.add(left, right)

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		left, right = diffs
		return np.add(left, right)

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		return (grad_value, grad_value)

class Negation(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Negation'

	@node_decorate('evaluate')
	def eval(self, values):
		return -1*np.array(values[0])

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		return -1*np.array(diffs[0])

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		return (-1*np.array(grad_value),)

class Subtraction(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Subtraction'

	@node_decorate('evaluate')
	def eval(self, values):
		# values vector respects order
		return np.subtract(values[0], values[1])

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		return np.subtract(diffs[0], diffs[1])

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		return (grad_value, -grad_value)


class Multiplication(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Multiplication'

	@node_decorate('evaluate')
	def eval(self, values):
		return np.multiply(values[0], values[1])

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		return np.multiply(diffs[0], values[1]) + np.multiply(diffs[1], values[0])

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		left, right = values
		left_out = np.multiply(right, grad_value)
		right_out = np.multiply(left, grad_value)
		return (left_out, right_out)

class Division(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Division'

	@node_decorate('evaluate')
	def eval(self, values):
		if values[1] == 0:
			raise ZeroDivisionError('Division by zero.')
		return np.divide(values[0], values[1])

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		num = np.multiply(diffs[0], values[1]) - np.multiply(values[0], diffs[1])
		denom = np.array(values[1])**2
		if denom == 0:
			raise ZeroDivisionError('Division by zero.')
		return np.divide(num, denom)

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		numer, denom = values
		numer_out = np.divide(grad_value, denom)
		denom_out = -1*np.divide(np.multiply(grad_value,numer), np.power(denom, 2))
		return (numer_out, denom_out)

class Power(Node):

	def __init__(self):
		super().__init__()
		self.type = 'Power'

	@node_decorate('evaluate')
	def eval(self, values):
		base, exp = values
		return np.power(base, exp)

	@node_decorate('differentiate')
	def diff(self, values, diffs):
		base, exp = values
		b_prime, exp_prime = diffs

		# First term
		coef = np.multiply(exp, b_prime)
		powered = np.power(base, np.subtract(exp, 1))
		term1 = np.multiply(coef, powered)

		# Second term
		term2 = 0

		# if exp_prime != 0:
			# Compute only if necessary, otherwise we run into log(-c) issues
		temp_base = np.copy(base)
		temp_base[temp_base<=0] = 1

		coef = np.multiply(np.log(temp_base), exp_prime)
		powered = np.power(base, exp)
		term2 = np.multiply(coef, powered)

		return term1+term2

	# Reverse mode
	@node_decorate('reverse')
	def reverse(self, values, grad_value):
		base, exp = values
		base_out = np.multiply(np.multiply(exp, np.power(base, exp-1)), grad_value)
		exp_out = np.multiply(np.multiply(np.log(base), np.power(base, exp)), grad_value)

		return (base_out, exp_out)