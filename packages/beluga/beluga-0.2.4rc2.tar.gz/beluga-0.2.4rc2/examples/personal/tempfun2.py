import numpy as np
from beluga.liepack.domain.liealgebras import so
from beluga.liepack.domain.liegroups import SO
from beluga.liepack.domain.hspaces import HManifold
from beluga.liepack.field import VectorField
from beluga.ivpsol import RKMK, Trajectory, Flow
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

y0 = np.eye(3)
tspan = [0, 2.5]

def M2eom(t, y):
    return (t ** 2, 1, -t)

def eom2g(t, y):
    x, y, z = M2eom(t, y)
    out = so(3)
    out.set_vector([x, y, z])
    return out

dim = y0.shape[0]
y = HManifold(SO(dim, y0))
vf = VectorField(y)
vf.set_M2g(eom2g)
ts = RKMK()
f = Flow(ts, vf)
ti, yi = f(y, tspan[0], tspan[-1], 0.1)
init = np.array([0, 0, 1])
gamma = Trajectory(ti, np.array([np.dot(_, init) for _ in yi]))

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(gamma.y[:,0], gamma.y[:,1], gamma.y[:,2])
plt.show()
