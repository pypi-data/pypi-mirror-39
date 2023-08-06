from Dotua.rautodiff import rAutoDiff as rad
from Dotua.roperator import rOperator as rop


ad = rad()
op = rop()
x,y = ad.create_rvector([[1, 2, 3], [1,3,6]])

a = x + 1
print(ad.partial(a,x))

h = op.sin(x)
print(ad.partial(h,x))

f = x + y
print(ad.partial(f,x))

f = 1 / (x[0] * x[1] * x[2]) + op.sin(1/x[0] + 1/x[1] + 1/x[2])
print(ad.partial(f,x[0]))
print(ad.partial(f,x[1]))
print(ad.partial(f,x[2]))