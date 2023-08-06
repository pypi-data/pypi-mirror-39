"""Brachistochrone example."""
import beluga
import logging
from math import pi

ocp = beluga.OCP('brachisto')

# Define independent variables
ocp.independent('t', 's')

# Define equations of motion
ocp.state('x', 'ti*v*cos(theta)', 'm') \
   .state('y', 'ti*v*sin(theta)', 'm') \
   .state('v', 'ti*g*sin(theta)', 'm/s')

# Define controls
ocp.control('theta', 'rad')

ocp.parameter('ti', 's')

# Define constants
ocp.constant('g', -9.81, 'm/s^2')
ocp.constant('x_f', 0, 'm')
ocp.constant('y_f', 0, 'm')

# Define costs
ocp.terminal_cost('ti', 's')

# Define constraints
ocp.constraints() \
    .initial('x', 'm')    \
    .initial('y', 'm') \
    .initial('v', 'm/s')  \
    .terminal('x-x_f', 'm')   \
    .terminal('y-y_f', 'm')

ocp.scale(m='y', s='y/v', kg=1, rad=1, nd=1)

bvp_solver = beluga.bvp_algorithm('Pseudospectral')
import numpy as np
from beluga.bvpsol import Solution
t = np.linspace(0,1,num=6)
y1 = np.linspace(0,0.1,num=6)
y2 = np.linspace(0,-0.1,num=6)
y3 = np.linspace(0,1,num=6)
q = np.array([])
u = np.array([np.linspace(-np.pi/2,-np.pi/2,num=6)]).T
solinit = Solution(t=t, y=np.column_stack((y1,y2,y3)), q=q, u=u)
solinit.dynamical_parameters = np.array([1])
solinit.aux['const'] = {'x_f': 0.1, 'y_f': -0.1, 'g':-9.81}

guess_maker = beluga.guess_generator('static', solinit=solinit)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection') \
                .num_cases(2) \
                .const('x_f', 1) \
                .const('y_f',-1)

beluga.add_logger(logging_level=logging.DEBUG, display_level=logging.DEBUG)

sol = beluga.solve(ocp,
             method='direct',
             bvp_algorithm=bvp_solver,
             steps=continuation_steps,
             guess_generator=guess_maker, autoscale=True)

import matplotlib.pyplot as plt

plt.plot(sol.y[:,0], sol.y[:,1])
plt.show()
