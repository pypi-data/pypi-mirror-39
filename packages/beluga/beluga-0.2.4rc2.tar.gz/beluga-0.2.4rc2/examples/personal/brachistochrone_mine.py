import numpy as np
from beluga.bvpsol.algorithms import Shooting
from beluga.bvpsol import Solution

def compute_control_reduced(t, X, params, consts):
    g = consts[0]
    lx = params[0]
    ly = params[1]
    v = X[0]
    lv = X[1]
    theta1 = 2*np.arctan((lx*v - np.sqrt(g**2*lv**2 - 2*g*lv*ly*v + lx**2*v**2 + ly**2*v**2))/(g*lv - ly*v))
    theta2 = 2*np.arctan((lx*v + np.sqrt(g**2*lv**2 - 2*g*lv*ly*v + lx**2*v**2 + ly**2*v**2))/(g*lv - ly*v))
    H1 = -g * lv * np.sin(theta1) + lx * v * np.cos(theta1) + ly * v * np.sin(theta1) + 1
    H2 = -g * lv * np.sin(theta2) + lx * v * np.cos(theta2) + ly * v * np.sin(theta2) + 1
    T = np.vstack((theta1,theta2))
    H = np.vstack((H1,H2))
    ind = np.argmin(H, axis=0)
    return T[ind][0]

def eqs_reduced(t,X,params,consts):
    g = consts[0]
    lx = params[0]
    ly = params[1]
    v = X[0]
    lv = X[1]
    # tf = X[2]
    tf = params[2]
    theta = compute_control_reduced(t,X,params,consts)
    return np.squeeze((-g*np.sin(theta)*tf, (-lx*np.cos(theta) - ly*np.sin(theta))*tf))

def quadratures(t, X, params, consts):
    v = X[0]
    lv = X[1]
    # tf = X[2]
    tf = params[2]
    lx = params[0]
    ly = params[1]
    theta = compute_control_reduced(t, X, params, consts)
    x = v*np.cos(theta)*tf
    y = v*np.sin(theta)*tf
    return (x,y)

def bcs_reduced(t0,X0,tf,Xf,quads0,quadsf,params,consts):
    bc1 = quads0[0]
    bc2 = quads0[1]
    bc3 = X0[0]
    bc4 = quadsf[0]-1
    bc5 = quadsf[1]+1
    bc6 = Xf[1]

    theta = compute_control_reduced(tf,Xf,params,consts)
    g = consts[0]
    x = quadsf[0]
    y = quadsf[1]
    v = Xf[0]
    lx = params[0]
    ly = params[1]
    lv = Xf[1]
    bc7 = -g * lv * np.sin(theta) + lx * v * np.cos(theta) + ly * v * np.sin(theta) + 1
    return (bc1,bc2,bc3,bc4,bc5,bc6,bc7)


algo = Shooting()
solinit = Solution()
solinit.t = np.linspace(0, 1, 2)
solinit.y = np.array([[0, -0.1], [0, -0.1]])
solinit.parameters = np.array([1])
out = algo.solve(eqs_reduced, quadratures, bcs_reduced, solinit)