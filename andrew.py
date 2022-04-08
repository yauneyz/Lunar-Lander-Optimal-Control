import numpy as np
from scipy.integrate import solve_bvp
from scipy.linalg import solve_continuous_are


class op_traject():
    def calc_approach(self, x0, y0, vx0, vy0, xf, yf, m, alpha, buf):
        yf = yf + buf
        # set up the right hand side of the ODE, with the parameter
        # tf (the final time rescaled)
        g = 9.8 / 1.5

        def rocket_ode(t, y, p):
            tf = p[0]
            out = tf * np.array([
                0 * y[0], 2 * alpha * y[5] - y[0], 0 * y[0], 2 * alpha * y[7] -
                y[2], y[5], y[1] / (2 * m**2), y[7], y[3] / (2 * m**2) - g
            ])

            return out

        # set up the endpoint conditions. The final one is H(tf) = 2a( -tf-1)
        def bc_new(ya, yb, p):

            H = -g*yb[3] + (yb[1]**2 + yb[3]**2)/(4*m**2) + yb[0] * \
                yb[5] - alpha*yb[5]**2 + yb[2]*yb[7] - alpha*yb[7]**2
            # bcs with inital velocity
            return np.array([
                ya[4] - x0, ya[6] - y0, ya[5] - vx0, ya[7] - vy0, yb[4] - xf,
                yb[6] - yf, yb[5], yb[7], H
            ])

        t = np.linspace(0, 1, 1000)
        y = np.zeros((8, t.size))
        self.res = solve_bvp(rocket_ode, bc_new, t, y, p=[1], max_nodes=20000)
        print(self.res.success)
        self.tf = self.res.p[0]
        self.yf = yf
        self.xf = xf
        self.buf = buf
        self.m = m

        self.traj = np.vstack((self.res.sol(np.linspace(0, 1, 200))[4],
                               self.res.sol(np.linspace(0, 1, 200))[6])).T

    def calc_land(self):
        y_goal = self.yf - buf
        x_goal = self.xf

    def get_goal(self, t):
        if t <= np.abs(self.tf):
            t = t / np.abs(self.tf)

            p1, p2, p3, p4, x, xv, y, yv = self.res.sol(t)
            return x, xv, y, yv, np.arctan2(
                -p4, p2), np.sqrt(p2**2 + p4**2) / (2 * self.m)


class PID():
    def __init__(self, Kp, Ki, Kd, MV_bar=0, dT=1e-2):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dT = dT
        self.I = 0
        self.e_prev = 0
        self.MV_bar = MV_bar

    def step(self, e):
        self.P = self.Kp * e
        self.I += self.Ki * e * dT
        self.D = self.Kd * (e - self.e_prev) / self.dT
        self.e_prev = e
        MV = self.MV_bar + self.P + self.I + self.D

        return MV


class Controller:
    def __init__(self, x0, y0, xv0, yv0, xf, yf, m, alpha, buf):

        self.A = np.array([[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1],
                           [0, 0, 0, 0]])
        self.B = np.array([[0, 0], [1 / m, 0], [0, 0], [0, 1 / m]])
        self.Q = np.diag([1e-6, 1e-10, 1e-6, 1e-10])
        self.R = np.diag([1 / 30, 1 / 30])
        self.P = solve_continuous_are(self.A, self.B, self.Q, self.R)
        self.u_opt = -np.linalg.inv(self.R) @ self.B.T @ self.P
        self.trajectory = op_traject()
        self.trajectory.calc_approach(x0, y0, xv0, yv0, xf, yf, m, alpha, buf)
        self.tf = self.trajectory.tf

    def get_control(self, t, x_actual, y_actual, xv_actual, yv_actual):
        x_target, xv_target, y_target, yv_target = self.trajectory.get_goal(
            t)[:4]

        state_err = np.array([
            x_actual - x_target, xv_actual + xv_target, y_actual - y_target,
            yv_actual + yv_target
        ])
        desired_f = self.u_opt @ state_err
        T_desired = np.linalg.norm(desired_f)
        theta_desired = np.arctan2(desired_f[0], desired_f[1])
        print("Goal Position", x_target, y_target)

        return theta_desired, T_desired
