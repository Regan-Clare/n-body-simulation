import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points


# defining initial conditions
NumParticles = 3  # number of particles
EM = 5.972e24  # Earth's Mass
G = 6.6743e-11  # Gravitational constant
dt = 0.1  # this is the time step. dt meaning change in time.

M = np.array([0.2*EM, EM, 10*EM])  # this 3x1 vector represents the mass of each

P = np.array([[1.5, 5],  # 3x2 matrix accounts for three particles and their relative initial positions. (x, y)
              [2, 5],
              [5, 5]])

v = np.array([[0, -2],  # 3x2 matrix accounts for three particles and their relative initial velocities (x, y)
              [20, -20],
              [0, 0]])

nP = np.array([], [])  # new position for x and y values


# add particles to canvas
ParticleColours = ['grey', 'green', 'yellow']  # colours of the particles
ParticleSizes = [20, 100, 1000]  # sizes of particles

# here, scatter is a method to plot objects and uses ax as a reference frame
# this means that when 'i' is the number of particles, then...
# the scatter method plots the position, size (s), and colour of the particles on the canvas
# the [i, 0] and [i, 1] extract the x and y coordinates of the i-th particle respectively.
# 0 being the first column x, and 1 being the second column y
# these basically refer back to the matrices/arrays I made earlier
for i in range(NumParticles):
    ax.scatter(P[i, 0], P[i, 1], s=ParticleSizes[i], color=ParticleColours[i])


def update(frame):
    global P
    global v

    # calculate pairwise distances between particles, subtract.outer() computes out level of products for vectors/arrays
    dx = np.subtract.outer(P[:, 0], P[:, 0])  # difference of [i, j] for x input
    dy = np.subtract.outer(P[:, 1], P[:, 1])  # difference of [i, j] for y input
    dr = np.sqrt(dx ** 2 + dy ** 2)  # uses element-wise sqrt to return non-negative sqrt of an array for each element
    # it calculates the sum of the squares of the elements dy and dx, giving pairwise distances between all particles

    # calculating pairwise gravitational forces using Newtons Law of Gravitation F = (G*mi*mj)/r^2
    fg = np.zeros_like(P)
    for i in range(NumParticles):  # for i particles
        for j in range(i + 1, NumParticles):  # for j particles
            F = G * M[i] * M[j] / dr[i][j] ** 2  # Newton's Universal Law of Gravitation
            fg[i] += F * (P[j] - P[i]) / dr[i][j]
            fg[j] += -F * (P[j] - P[i]) / dr[i][j]

    # this updates the acceleration, velocity, and position of each particle
    acceleration = fg / M[:, np.newaxis]  # F = ma (Newton's Second Law)
    v += acceleration * dt  # a = v/t => v = a*t
    P += v * dt  # position changes with respect to velocity over a change in time

    for i in range(NumParticles):
        nP[i] += dt * P[i, 0]
        nP[i] += dt * P[i, 1]
        nP[i].append(P[i, 0])
        nP[i].append(P[i, 1])


meh = anim.FuncAnimation(fig, update, interval=1, blit=True, frame=200)


plt.show()