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

def H(x, y):
    return x**2 + y**2

def dH(x, y):
    return (2*x, 2*y)

x = so(2)
x.random()

print(x)
print(x.get_vector())


# y0 = np.array([0])
#
# space0 = np.eye(1)
#
# def fm2g(t, y):
#     dat = np.array([[0, t, 1], [-t, 0, -t**2], [-1, t**2, 0]])
#     keyboard()
#     return so(3, dat)
#
# dim = y0.shape[0]
# y = HLie(SO(dim), space0)
# vf = VectorField(y)
# vf.set_equationtype('general')
# vf.set_M2g(fm2g)
# ts = RKMK()
#
# f = Flow(ts, vf, variablestep=True)
# ti, yi = f(y, 0, 2.5, 0.01)
# gamma = Trajectory(ti, np.vstack([np.dot(_.data, y0) for _ in yi]))
#
# plt.plot(gamma.y[:,0], gamma.y[:,1])
#
# # plt.plot(gamma.t[1:] - gamma.t[:-1])
# plt.show()
