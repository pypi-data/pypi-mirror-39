from beluga.ivpsol import Propagator

from beluga.liepack.domain.liealgebras import so
from beluga.liepack.domain.liegroups import SO
from beluga.liepack.domain.hspaces import HLie
from beluga.liepack.field import VectorField
from beluga.liepack import exp, Adjoint, Commutator
from beluga.ivpsol import RKMK, Flow

from beluga.ivpsol import Trajectory

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

y0 = np.array([0,0,1])

space0 = np.eye(3)

def fm2g(t, y):
    dat = np.array([[0, t, 1], [-t, 0, -t**2], [-1, t**2, 0]])
    return so(3, dat)

dim = y0.shape[0]
y = HLie(SO(dim), space0)
vf = VectorField(y)
vf.set_equationtype('general')
vf.set_M2g(fm2g)
ts = RKMK()
ts.setmethod('trap2')
f = Flow(ts, vf, variablestep=False)
ti, yi = f(y, 0, 2.5, 0.1)
gamma = Trajectory(ti, np.vstack([np.dot(_.data, y0) for _ in yi]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(gamma.y[:,0], gamma.y[:,1], gamma.y[:,2])

print(gamma.y)

# plt.plot(gamma.t[1:] - gamma.t[:-1])
plt.show()

# x = so(3)
# y = so(3)
# z = so(3)
#
# M = SO(3)
#
# x.set_vector([1, 0, 0])
# y.set_vector([0, 1, 0])
# z.set_vector([0, 0, 1])
#
# rot = np.pi/4
# M.set_data(exp(x*rot).data)
#
# AdG = Adjoint(M)
#
# print(Adjoint(M,y).data)
# n1 = np.linalg.norm(y.get_vector())
# n2 = np.linalg.norm(z.get_vector())
# print((Adjoint(M,y).data - (y+z).data/(np.sqrt(n1**2 + n2**2)) < 1e-15))
# print(z.data)

# M.set_data(exp(x*np.pi/4).data)
# Ad = Adjoint(M)
# keyboard()
# print(M.data)

# p = Propagator(algorithm='lie', maxstep=0.02)

# gam = p(fm2g, None, [0, 5], y0, None)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(gam.y[:,0], gam.y[:,1], gam.y[:,2])

# plt.plot(gam.t[1:] - gam.t[:-1])
# plt.show()
# print(gam.y.shape)

# print(ts)

# print(ts(vf, np.eye(3),0,0.5))
