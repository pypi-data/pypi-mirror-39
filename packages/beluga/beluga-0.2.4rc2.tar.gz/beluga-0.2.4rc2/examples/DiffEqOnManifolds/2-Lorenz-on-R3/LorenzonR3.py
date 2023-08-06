import numpy as np
from beluga.liepack import exp
from beluga.liepack.domain.liealgebras import rn
from beluga.liepack.domain.liegroups import RN
from beluga.liepack.domain.hspaces import HManifold
from beluga.liepack.field import VectorField
from beluga.ivpsol import RKMK, Trajectory, Flow
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

temp = rn(4)
temp.set_vector([25,0,-20])
y0 = exp(temp)

tspan = [0, 2.5]

def M2g(t, y):
    sigma = 10
    rho = 28
    beta = 8/3
    out = rn(4)
    [[-beta, 0, y(2)], [0, -sigma, sigma], [-y(2), rho, -1]]
    out.set_vector([x, y, z])
    return out

dim = y0.shape[0]
y = HManifold(RN(dim, y0))
vf = VectorField(y)
vf.set_M2g(M2g)
ts = RKMK()
f = Flow(ts, vf)
ti, yi = f(y, tspan[0], tspan[-1], 0.1)
init = np.array([0, 0, 1])
gamma = Trajectory(ti, np.array([np.dot(_, init) for _ in yi]))

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(gamma.y[:,0], gamma.y[:,1], gamma.y[:,2])
plt.show()
