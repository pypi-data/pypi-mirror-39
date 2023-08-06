import beluga
import logging
from math import pi, sqrt

ocp = beluga.OCP('timeoptimallaunch')

g = 9.80665
h = 180000
Vc = sqrt(3.9860044e5/(6378.14 + h/1000))*1000
h_scale = 8440
rho0 = 1.225
A = 7.069
Cd = 0
eta = rho0*Cd*A/2
beta = h/h_scale
f = 2.1e6
m0 = 60880
mdot = 0
delta_tf = 0
tfguess = 700

# Define independent variables
ocp.independent('t', 's')

# Define equations of motion
ocp.state('x', 'vx', 'm') \
   .state('y', 'vy', 'm') \
   .state('vx', 'F / mass * cos(theta) - D / mass * vx / sqrt(vx**2 + vy**2)', 'm/s') \
   .state('vx', 'F / mass * sin(theta) - D / mass * vy / sqrt(vx**2 + vy**2) - g', 'm/s') \

# Define controls
ocp.control('theta','rad')

# Define constants
ocp.constant('g', g, 'm/s^2')

# Define costs
ocp.path_cost('1', '1')

# Define constraints
ocp.constraints() \
    .initial('x-x_0', 'm')    \
    .initial('y-y_0', 'm') \
    .initial('v-v_0', 'm/s')  \
    .terminal('x-x_f', 'm')   \
    .terminal('y-y_f', 'm')

# Use the "adjoined method" to solve for the constraints. (Default is False)
ocp.constraints().set_adjoined(True)

ocp.scale(m='y', s='y/v', kg=1, rad=1, nd=1)

bvp_solver = beluga.bvp_algorithm('Shooting',
                        derivative_method='fd',
                        tolerance=1e-4,
                        max_iterations=200,
                        max_error=100,
                        num_arcs=1,
                        num_cpus=1
             )

guess_maker = beluga.guess_generator('auto',
                start=[0,0,0],          # Starting values for states in order
                direction='forward',
                costate_guess = -0.1,
                control_guess=[-pi/2],
                use_control_guess=True,
)

continuation_steps = beluga.init_continuation()

continuation_steps.add_step('bisection') \
                .num_cases(21) \
                .terminal('x', 10) \
                .terminal('y',-10)

beluga.add_logger(logging_level=logging.DEBUG)

sol = beluga.solve(ocp,
             method='traditional',
             bvp_algorithm=bvp_solver,
             steps=continuation_steps,
             guess_generator=guess_maker)
