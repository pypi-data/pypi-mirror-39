import numpy as np
from Dotua.nodes.vector import Vector

'''
Test for vector variable basic functions and the jacobian of vector function to vector
'''

# Define vector objects
x = Vector([1,2])
y = Vector([0,1])
z = Vector([2,1])
a = Vector([0,0])
b = Vector([1,1])
c = Vector([1,0])

f_1 = x[0] + x[1]
f_2 = x[0] - 3 - x[1] - x[1]
f_3 = 1 + x[1] - x[0] * x[1] - x[0] - 3
f_4 = 3 / x[0] + (x[0] * x[1]) / 2 - 4 * x[1]
f_5 = x[0] ** 3 + x[1] / x[0]
f_6 =  2 ** x[1]
f_7 = 3 + x + y - 2
f_8 = -1 - x - y - 3
f_9 = 3 * x + y * 2 + x * y
f_10 = y / 3 + 2 / x + y / x
f_11 = z + x
f_12 = z + a
f_13 = f_11 + f_12
f_14 = b - 1
f_15 = f_11 - f_12
f_16 = c - f_11
f_17 = f_11 - x
f_18 = f_11 * 2
f_19 = f_12 * f_14
f_20 = x * f_12
f_21 = f_12 * x
f_22 = z + f_12
f_23 = x / f_12
f_24 = f_12 / x
f_25 = f_12 / f_15
f_26 = f_12 / 2
f_27 = x - y
f_28 = 2 / f_12
f_29 = - f_12
f_30 = x ** 3
f_31 = f_12 ** 2
f_32 = x ** z
f_33 = f_12 ** z
f_34 = x ** f_12
f_35 = f_11 ** f_12
f_36 = 2 ** x
f_37 = 2 ** f_11

d = Vector([2,2])
f_38 = 1 - d[0]
f_39 = d[0] ** d[1]

def test_sub():
	assert(f_38.partial(d[0]) == -1)
	assert(f_38.partial(d[1]) == 0)
	assert(f_39.partial(d[0]) == 4)
	assert(f_39.partial(d[1]) == 4*np.log(2))

def test_rpow():
	assert(f_6.partial(x[0]) == 0)
	assert(f_6.partial(x[1]) == 4*np.log(2))

def test_vector_pow():
	assert(f_30.eval() == [1,8])
	assert(f_31.eval() == [4,1])
	assert(f_32.eval() == [1,2])
	assert(f_33.eval() == [4,1])
	assert(f_34.eval() == [1,2])
	assert(f_35.eval() == [9,3])
	assert(f_36.eval() == [2,4])
	assert(f_37.eval() == [8,8])


def test_vector_add():
	assert(f_7.eval() == [2,4])
	assert(f_11.eval() == [3,3])
	assert(f_12.eval() == [2,1])
	assert(f_13.eval() == [5,4])
	assert(f_22.eval() == [4,2])

def test_vector_sub():
	assert(f_8.eval() == [-5,-7])
	assert(f_14.eval() == [0,0])
	assert(f_15.eval() == [1,2])
	assert(f_16.eval() == [-2,-3])
	assert(f_17.eval() == [2,1])
	assert(f_27.eval() == [1,1])

def test_vector_times():
	assert(f_9.eval() == [3,10])
	assert(f_18.eval() == [6,6])
	assert(f_19.eval() == [0,0])
	assert(f_20.eval() == [2,2])
	assert(f_21.eval() == [2,2])

def test_vector_divide():
	assert(f_10.eval() == [2,11/6])
	assert(f_23.eval() == [0.5,2])
	assert(f_24.eval() == [2,0.5])
	assert(f_25.eval() == [2,0.5])
	assert(f_26.eval() == [1,0.5])
	assert(f_28.eval() == [1,2])

def test_neg():
	assert(f_29.eval() == [-2,-1])

def test_repr():
	print(x)

# Define a vector function and get a jacobian of the vector function to vector

#f = [f_1, f_2, f_3, f_4, f_5]
#jacobian = []

#for function in f:
	#jacobian.append(function.eval()[1])

#def test_jacobian():
	#assert(jacobian == [[1,1], [1,-2], [-3,0], [-2,-3.5], [1,1]])

