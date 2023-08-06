# Optimization Suite for DeriveAlive module
# Harvard University, CS 207, Fall 2018
# Authors: Chen Shi, Stephen Slater, Yue Sun

import DeriveAlive as da
import numpy as np

# User-defined variable
x_var = da.Var([2.00])
y_var = da.Var([0])
z_var = da.Var([1])

def f(var):
	return (var - 1) ** 2 - 1

def NewtonRoot(f, x0, tol=1e-7, iters=1000):
	is_vec_input = len(x0.val) > 1

	print ("inside NewtonRoot, init guess is:\n{}".format(x0))

	# Run Newton's root-finding method
	x = x0
	
	# Check if initial guess is a root
	g = f(x)
	if np.array_equal(g.val, np.zeros((g.val.shape))):
		return da.Var(x.val, g.der)

	for i in range(iters):
		g = f(x)
		if np.array_equal(g.der, np.zeros((g.der.shape))):
			g = g + tol * x0
		step = da.Var(g.val / g.der, None)

		# If step size is below tolerance, then no need to update step
		cond = np.linalg.norm(step.val) if is_vec_input else abs(step)
		print ("condition: {}".format(cond))
		if cond < tol:
			print ("Reached tol in {} iterations".format(i))
			break
		print ("x is:\n{}".format(x))
		x = x - step
	else:
		print ("Reached {} iterations without satisfying tolerance.".format(iters))

	return da.Var(x.val, g.der)


def NewtonOptimization(f, x0, tol=1e-7, iters=1000):
	pass


def SteepestDescent(f, x0, tol=1e-7, iters=1000):
	pass

# for x in range(-1, 5):
# 	x_var = da.Var(x)
# 	print ("\n")
# 	print (NewtonRoot(f, x_var))


# Attempt at vector case
# x = da.Var(1, [1, 0])
# y = da.Var(1, [0, 1])
# init_guess = da.Var([x, y])

# h = vec ** 2
# x = vec.val[0]
# y = vec.val[1]
# return da.Var(x ** 2 + y ** 2, [vec.der[:, 0] + vec.der[:, 1]])

# Vector ideas
# x = da.Var(1, [1, 0])
# y = da.Var(1, [0, 1])
# init_guess = da.Var([x, y])

# h = vec ** 2
# x = vec.val[0]
# y = vec.val[1]
# return da.Var(x ** 2 + y ** 2, [vec.der[:, 0] + vec.der[:, 1]])


def r2_to_r2():
	init_guess = da.Var([1, 2], [1, 1])

	def z(vec):
		return vec ** 2

	print ("\n\nTRYING R2 -> R2 CASE. EXPECT ROOT AT (0, 0) FOR Z(X, Y) = [X**2, Y**2].\n")
	print (NewtonRoot(z, init_guess))


def r2_to_r1():
	# init_guess = da.Var([1, 2], [1, 1])
	x = vec.val[0]
	y = vec.val[1]
	init_guess = [x, y]

	def z(vec):
		return da.Var(vec.val[0] + vec.val[1], [vec.der[0] + vec.der[1]])

	def z(vec):
		return vec[0] + vec[1]
		return x + y

	print ("\n\nTRYING R2 -> R1 CASE. EXPECT ROOT AT (0, 0) FOR Z(X, Y) = X + Y.\n")
	print (NewtonRoot(z, init_guess))


# r2_to_r2()
r2_to_r1()

	# Set plot limits to cover entire range of path taken
	# plt.xlim(min(x_min, min(x_path) - 1), max(x_max, max(x_path) + 1))
	# plt.ylim(min(y_min, min(y_path) - 1), max(y_max, max(y_path) + 1))


list of Vars -> Var([Var, Var])

	# #def F(x):
	# #        return da.Var(
	# #            [x[0]**2 - x[1] + x[0]* np.cos(np.pi*x[0]),
	# #             x[0]*x[1] + np.exp(-x[1]) - x[0]**2])

	# #expected = np.array([1, 0])
	# #x1=da.Var([2],[1, 0])
	# #x2=da.Var([-1],[0, 1])
	# #x = da.Var([x1, x2])

	# def F(x1, x2):
	#         return da.Var(
	#             [x1 ** 2 - x2 + x1 * np.cos(np.pi*x1),
	#              x1 * x2 + np.exp(-x2) - x1 ** 2])
	# x1=da.Var([2],[1, 0])
	# x2=da.Var([-1],[0, 1])
	# x = da.Var([x1, x2])
	# output = NewtonRoot(F(x1, x2), x)

	# init_guess = da.Var([1, 2], [1, 1])
	# x = vec.val[0]
	# y = vec.val[1]
	# init_guess = [x, y]

	# def z(variables):
	# 	x, y = variables
	# 	# return da.Var(vec.val[0] + vec.val[1], [vec.der[0] + vec.der[1]])
	# 	return x + y

	# def z(vec):
	# 	return vec[0] + vec[1]
	# 	return x + y


# def test_r2_to_r2():
# 	init_guess = da.Var([1, 2], [1, 1])

# 	def z(vec):
# 		return vec ** 2

# 	print ("\n\nTRYING R2 -> R2 CASE. EXPECT ROOT AT (0, 0) FOR Z(X, Y) = [X**2, Y**2].\n")
# 	print (rf.NewtonRoot(z, init_guess))


	if f == 'mse' and len(data) > 0:
		num_points = len(data)
		num_features = len(data[0]) - 1
		num_weights = num_features + 1
		assert num_features == len(x) if isinstance(x, list) else 1

		# Initialize weights to 0
		weights = [da.Var(0, _get_unit_vec(num_weights, i)) for i in range(num_weights)]

		y = data[:, -1]
		X = data[:, :-1]

		def f(weights):
			return (1 / 2 * num_points) * sum([weights[0] + np.dot(weights[1:], X[i]) for i in range(num_points)])

		f_string = '0.5 * MSE'



	def logistic(self):
		val = 1 / (1 + np.exp(-self.val))
		if len(self.der.shape) == 0:
			der = None
		else:
			# self is a Var of a scalar or vector
			der_vals = np.exp(self.val) / ((1 + np.exp(self.val)) ** 2)
			der = np.zeros(self.der.shape)
			print ("self:\n{}".format(self))
			print ("der_vals: {}".format(der_vals))
			print ("der: {}".format(der))
			# for i in range(len(der)):
			# 	for j in range()
			# 	der[i] = der_vals[i] * self.der[i]

		return Var(val, der)


	def case_8():
		'''Find the roots of a more complicated function from R^3 to R^1.'''

		def f(variables):
			x, y, z = variables
			return x ** (y ** 2) - z ** 2

		f_string = 'f(x, y, z) = x^(y^2) - z^2'

		for x_val, y_val, z_val in [[1, -2, 5], [2, 4, -5]]:
			x0 = da.Var(x_val, [1, 0, 0])
			y0 = da.Var(y_val, [0, 1, 0])
			z0 = da.Var(z_val, [0, 0, 1])
			init_vars = [x0, y0, z0]
			solution, xyz_path, f_path = rf.NewtonRoot(f, init_vars)
			m = len(solution.val)
			xn, yn, zn = solution.val
			rf.plot_results(f, xyz_path, f_path, f_string, fourdim=True)

			# root: x = +- (zn^2)^(1 / (yn^2))
			root_1 = (zn ** 2) ** (1 / (yn ** 2))
			root_2 = -root_1
			assert (np.allclose(xn, root_1) or np.allclose(xn, root_2))

			# dfdx = y^2 * x^{y^2 - 1}
			# dfdy = 2yx^{y^2} * log(x)
			# dfdz = -2z
			der = [yn ** 2 * (xn ** ((yn ** 2) - 1)), 
				   2 * yn * (xn ** (yn ** 2)) * np.log(xn), 
				   -2 * zn]

			# TODO: add check for derivative once __pow__ is updated.
			# assert np.allclose(solution.der, der)	

	def case_8():
		'''Find the roots of a more complicated function from R^3 to R^1.'''

		def f(variables):
			x, y, z = variables
			return x ** (y ** 2) - z ** 2

		f_string = 'f(x, y, z) = x^(y^2) - z^2'

		for x_val, y_val, z_val in [[1, -2, 5], [2, 4, -5]]:
			x0 = da.Var(x_val, [1, 0, 0])
			y0 = da.Var(y_val, [0, 1, 0])
			z0 = da.Var(z_val, [0, 0, 1])
			init_vars = [x0, y0, z0]
			solution, xyz_path, f_path = rf.NewtonRoot(f, init_vars)
			m = len(solution.val)
			xn, yn, zn = solution.val
			rf.plot_results(f, xyz_path, f_path, f_string, fourdim=True)

			# root: x = +- (zn^2)^(1 / (yn^2))
			root_1 = (zn ** 2) ** (1 / (yn ** 2))
			root_2 = -root_1
			assert (np.allclose(xn, root_1) or np.allclose(xn, root_2))

			# dfdx = y^2 * x^{y^2 - 1}
			# dfdy = 2yx^{y^2} * log(x)
			# dfdz = -2z
			der = [yn ** 2 * (xn ** ((yn ** 2) - 1)), 
				   2 * yn * (xn ** (yn ** 2)) * np.log(xn), 
				   -2 * zn]

			# TODO: add check for derivative once __pow__ is updated.
			# assert np.allclose(solution.der, der)	


