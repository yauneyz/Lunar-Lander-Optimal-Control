import pudb
from andrew import Controller
from matplotlib import pyplot as plt

state = [200, 0, 0, 0, 0, 0]
x_f = 0
y_f = -640

control = Controller(*state, 1, 1e-1, 5)
trajectory = control.trajectory.traj

plt.plot(trajectory[:, 0], trajectory[:, 1])
plt.show()

# pudb.set_trace()
# t, y, u = resp.time, resp.x, resp.inputs

# plt.subplot(3, 1, 1)
# plt.plot(y[0], y[1])
# plt.xlabel("x [m]")
# plt.ylabel("y [m]")

# plt.subplot(3, 1, 2)
# plt.plot(t, u[0])
# plt.axis([0, 10, 9.9, 10.1])
# plt.xlabel("t [sec]")
# plt.ylabel("u1 [m/s]")

# plt.subplot(3, 1, 3)
# plt.plot(t, u[1])
# plt.axis([0, 10, -0.01, 0.01])
# plt.xlabel("t [sec]")
# plt.ylabel("u2 [rad/s]")

# plt.suptitle("Lane change manuever")
# plt.tight_layout()
# plt.show()
