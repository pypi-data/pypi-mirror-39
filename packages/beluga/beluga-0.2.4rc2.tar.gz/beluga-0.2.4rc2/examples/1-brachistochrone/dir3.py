from beluga.bvpsol.algorithms import Pseudospectral
# from beluga.bvpsol.algorithms import BaseAlgorithm
import copy
from scipy.optimize import minimize
from beluga.bvpsol.algorithms.Pseudospectral import lglweights, lglnodes, lglD, lpoly, _cost, _eq_constraints
from beluga.ivpsol import Trajectory
import numpy as np

t = np.linspace(0,1,num=10)
y = np.linspace(0,0,num=10)
y = np.column_stack((y,y))
u = np.array([np.linspace(0,0,num=10)]).T

def eoms(t,x,u,p,aux):
    return (x[1],u[0])

def bcs(t0,x0,q0,u0,tf,xf,qf,uf,p,dnp,aux):
    return (x0[0]-0,xf[0]-0,x0[1]-1,xf[1]+1)

def path_cost(t,x,u,p,aux):
    return u[0]**2

def constraints_ineq(t,x,u,p,aux):
    y1 = x[0]
    return y1 - 1/9

solinit = Trajectory(t,y,np.array([]),u)
solinit.dynamical_parameters = np.array([])
solinit.nondynamical_parameters = np.array([])
solinit.aux = None

ps = Pseudospectral()
ps.set_derivative_function(eoms)
ps.set_boundarycondition_function(bcs)
ps.set_path_cost_function(path_cost)
ps.set_inequality_constraint_function(constraints_ineq)

tau = lglnodes(10-1)
D = lglD(tau)
weights = lglweights(tau)

arrrgs = (eoms, bcs, path_cost, 2, 1, weights, D, 1, 0, 10, [])

cons1 = {'type': 'eq', 'fun': _eq_constraints, 'args': arrrgs}
Xinit = np.hstack((y[:,0],y[:,1],u[:,0]))

sol = ps.solve(solinit)

import matplotlib.pyplot as plt


plt.plot(sol.t, sol.y[:,0], marker='o')
t = np.linspace(sol.t[0], sol.t[-1], num=20)
from scipy.interpolate import lagrange
plt.plot(t, LagrangeInter(np.array([0,    0.0402,    0.1306,    0.2610,    0.4174,    0.5826,    0.7390,    0.8694,    0.9598,    1.0000]), np.array([0,    0.0356,    0.0862,    0.1111,    0.1111,    0.1111,    0.1111,    0.0862,    0.0356,         0]), np.array([0,    0.0526,    0.1053,    0.1579,    0.2105,    0.2632,    0.3158,    0.3684,    0.4211,    0.4737,    0.5263,    0.5789,    0.6316,    0.6842, 0.7368,    0.7895,    0.8421,    0.8947,    0.9474,    1.0000])))
plt.show()

