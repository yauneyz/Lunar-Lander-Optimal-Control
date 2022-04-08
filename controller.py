import numpy as np
import control as ct
import control.optimal as opt
import matplotlib.pyplot as plt


# Compute the state evolution of the rocket
def rocket_update(t, x, u, params):
    # Return the derivative of the state
    return np.array([
        x[2],
        x[3],
        x[5] * np.cos(x[4]),
        x[5] * np.sin(x[4]),
        u[0],
        u[1],
    ])


def rocket_output(t, x, u, params):
    return x  # return x, y, theta (full state)


# Define the rocket landing dynamics as an input/output system
rocket = ct.NonlinearIOSystem(rocket_update,
                              rocket_output,
                              states=6,
                              name='rocket',
                              inputs=('dtheta', 'dT'),
                              outputs=('x', 'y', 'xp', 'yp', 'theta', 'T'))


def get_control(x, y, xp, yp, theta, T, x_f, y_f):
    """
    Finds the optimal path for landing at a particular spot on the map
    """
    x0 = [x, y, xp, yp, theta, T]
    xf = [x_f, y_f, 1, 1, 0, 0]
    u0 = [0, 0]
    uf = [0, 0]
    Tf = 1

    Q = np.diag([0, 0, 0, 0, 0, 100])
    R = np.diag([1, 1])
    P = np.diag([1000, 1000, 1000, 1000, 1000, 0])
    traj_cost = opt.quadratic_cost(rocket, Q, R, x0=xf, u0=uf)
    term_cost = opt.quadratic_cost(rocket, P, 0, x0=xf)

    constraints = [opt.input_range_constraint(rocket, [-1, 1], [-1, 1])]

    horizon = np.linspace(0, Tf, 20, endpoint=True)
    result = opt.solve_ocp(rocket,
                           horizon,
                           x0,
                           traj_cost,
                           constraints,
                           terminal_cost=term_cost,
                           initial_guess=u0)

    u_theta, u_T = result.inputs

    # Determine the control
    right = (u_theta[0] > 0)
    left = not right
    up = (u_T[0] > 0)
    down = not up

    print("Control raw:", u_theta[0], u_T[0])

    if u_theta[0] == 0:
        left = False
        right = False

    if u_T[0] == 0:
        down = False
        up = False

    return result
    # return left, right, down, up
