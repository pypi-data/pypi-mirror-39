from beluga.ivpsol import Propagator

from beluga.liepack.domain.liealgebras import sp
from beluga.liepack.domain.liegroups import SP, RN
from beluga.liepack.domain.hspaces import HLie
from beluga.liepack.field import VectorField
from beluga.liepack import exp, Adjoint, commutator
from beluga.ivpsol import RKMK, Flow

from beluga.ivpsol import Trajectory

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from beluga.utils import Bernoulli
from scipy.special import bernoulli as B2


y0 = np.array([1,1])

space0 = np.eye(3)
space0[0,2] = y0[0]
space0[1,2] = y0[1]

basis = sp(2).basis()
breakpoint()
def fm2g(t, y):
    omega = basis[1] - basis[2]
    til = 0*basis[0] + basis[2]
    return sp(2, omega + til)

# dx ^ dy = dxdy - dydx => [[0, 1], [-1, 0]]

# H = x^2/a + y^2/b
# dH = 2x/a dx + 2y/b dy
#

dim = y0.shape[0]
y = HLie(RN(dim), space0)
y = RN(dim)
vf = VectorField(y)
vf.set_equationtype('general')
vf.set_M2g(fm2g)
ts = RKMK()
ts.setmethod('rk45')
f = Flow(ts, vf, variablestep=False)
ti, yi = f(y, 0, 8*np.pi, 0.1)
for ii in np.linspace(0.5, 1.5, 10):
    y0 = np.array([ii,ii])
    gamma = Trajectory(ti, np.vstack([_.data @ y0 for _ in yi]))
    plt.plot(gamma.y[:,0], gamma.y[:,1])
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(gamma.y[:,0], gamma.y[:,1], gamma.y[:,2])
#
# print(gamma.y)


plt.show()
