import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points

# defining initial conditions
EM = 5  # 5.972e24 Earth's Mass
G = 6.6743e-11  # Gravitational constant
dt = 0.1  # this is the time step. dt meaning change in time.
NumParticles = int(input("How many particles in this system?: "))

m = [EM] * NumParticles
P = np.random.rand(NumParticles, 2) * 9.8  # initial positions [x, y], at 9.8 so, it doesn't hit the edge
v = np.zeros((NumParticles, 2))  # initial velocities [dx, dy]
dP = []  # new positions [cy, cx]

curve, = ax.plot([], [])
obj, = plt.plot([], [])


def initial_conditions():
    curve.set_data([], [])
    obj.set_data([], [])
    return curve, obj,


initial_conditions()

# here, scatter is a method to plot objects and uses ax as a reference frame
# this means that when 'i' is the number of particles, then...
# the scatter method plots the position, size (s), and colour of the particles on the canvas
# the [i, 0] and [i, 1] extract the x and y coordinates of the i-th particle respectively.
# 0 being the first column x, and 1 being the second column y
# these basically refer back to the matrices/arrays I made earlier
for i in range(NumParticles):
    ax.scatter(P[i, 0], P[i, 1], s=40, c='black')  # x-position, y-position, size, colour


def update(frame):
    global P, v, r
    for i in range(2):
        j = (i + 1) % 2
        v[i, 0] += dt * m[j] * (P[j, 0] - P[i, 0]) / ((P[j, 0] - P[i, 0]) ** 2 + (P[j, 1] - P[i, 1]) ** 2) ** 1.5
        v[i, 1] += dt * m[j] * (P[j, 1] - P[i, 1]) / ((P[j, 0] - P[i, 0]) ** 2 + (P[j, 1] - P[i, 1]) ** 2) ** 1.5
        v[2, 0] += dt * m[i] * (P[i, 0] - P[2, 0]) / ((P[i, 0] - P[2, 0]) ** 2 + (P[i, 1] - P[2, 1]) ** 2) ** 1.5
        v[2, 1] += dt * m[i] * (P[i, 1] - P[2, 1]) / ((P[i, 0] - P[2, 0]) ** 2 + (P[i, 1] - P[2, 1]) ** 2) ** 1.5
    for i in range(3):
        P[i, 0] += dt * v[i, 0]
        P[i, 1] += dt * v[i, 1]
        dP[i].append(P[i, 0])
        dP[i].append(P[i, 1])
    curve.set_data(dP[i])
    obj.set_data(P[i, 0], P[i, 1])
    return curve, obj,


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=True, save_count=9000)

plt.show()