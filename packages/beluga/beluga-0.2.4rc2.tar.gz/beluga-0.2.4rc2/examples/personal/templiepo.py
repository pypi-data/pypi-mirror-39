from beluga.liepack.domain.liealgebras import *
import numpy as np
from matplotlib import pyplot as plt
from sympy.diffgeom import Manifold, Patch, CoordSystem, WedgeProduct, TensorProduct, Commutator, covariant_order, Differential
from math import floor

M = Manifold('M', 2)
P = Patch('P',M)
C = CoordSystem('C', P, names=['x','y'])

coord = C.coord_functions()
dx = C.base_oneforms()
Dx = C.base_vectors()

omega = 0
pi = 0
n = len(coord)
for ii in range(floor(n/2)):
    omega += WedgeProduct(dx[ii], dx[ii+floor(n / 2)])
    pi += WedgeProduct(Dx[ii], Dx[ii + floor(n / 2)])

func = coord[0]
hamiltonian = coord[0]**2 + coord[1]**2

def X_(arg):
    return pi.rcall(None, arg)


def d(f):
    order = covariant_order(f)
    if order == 0:
        return sum([Differential(f)(D_x) * dx for (D_x, dx) in zip(Dx, dx)])

def sharp(f):
    set1d = dict(zip(dx, Dx))
    return f.subs(set1d, simultaneous=True)

def flat(f):
    set1D = dict(zip(Dx, dx))
    return f.subs(set1D, simultaneous=True)

X_x = X_(func)
X_H = X_(hamiltonian)

system = Commutator(sharp(d(func)), sharp(d(hamiltonian)))

breakpoint()

tol = 1e-4

g = rn(3)

g_basis = g.basis()
x = g_basis[0]
y = g_basis[1]

gs_basis = [np.array([1,0]), np.array([0,1])]
xs = gs_basis[0]
ys = gs_basis[1]


def h(gs):
    return gs[0]**2 + gs[1]**2

def F(gs):
    return gs[0]

def dh(gs):
    out = LieAlgebra(g)
    out.set_vector([2*gs[0], 2*gs[1]])
    return out

def df(gs):
    out = LieAlgebra(g)
    out.set_vector([1, 0])
    return out

def lbfh(gs):
    out = LieAlgebra(g)
    out.set_vector([2, 0])
    return out

p1 = x
p1s = xs

def pair(f,g):
    return np.dot(f, g.get_vector())

print(pair(xs,lbfh(xs)))