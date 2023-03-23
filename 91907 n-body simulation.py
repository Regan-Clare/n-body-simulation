import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import math  # allows the use of mathematical constants
from matplotlib.animation import FuncAnimation  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points

# defining initial conditions

NumParticles = 3  # number of particles
EM = 5.972e24  # Earth's Mass
G = 6.6743e-11  # Gravitational constant
dt = 0.1  # this is the time step. dt meaning change in time.

# this 3x1 vector represents the mass of each
mass = np.array([EM, 2*EM, 3*EM])

# 3x2 matrix accounts for three particles and their relative positions
position = np.array([[7, 5],
                     [2, 5],
                     [5, 5]])

# 3x2 matrix accounts for three particles and their relative velocities
velocity = np.array([[2, 2],
                     [-2, -2],
                     [0, 0]])


# add particles to canvas
ParticleColours = ['red', 'green', 'blue']  # colours of the particles
ParticleSizes = [50, 100, 150]  # sizes of particles

# here, scatter is a method to plot objects and uses ax as a reference frame
# this means that when 'i' is the number of particles, then...
# the scatter method plots the position, size (s), and colour of the particles on the canvas
# the [i, 0] and [i, 1] extract the x and y coordinates of the i-th particle respectively.
# 0 being the first column x, and 1 being the second column y
# these basically refer back to the matrices/arrays I made earlier
for i in range(NumParticles):
    ax.scatter(position[i, 0], position[i, 1], s=ParticleSizes[i], color=ParticleColours[i])


def update():
    global position
    global velocity

    # calculate pairwise distances between particles, subtract.outer() computes out level of products for vectors/arrays
    dx = np.subtract.outer(position[:, 0], position[:, 0])  # difference of [i, j] for x input
    dy = np.subtract.outer(position[:, 1], position[:, 1])  # difference of [i, j] for y input
    dr = np.sqrt(dx ** 2 + dy ** 2)  # uses element-wise sqrt to return non-negative sqrt of an array for each element
    # it calculates the sum of the squares of the elements dy and dx, giving pairwise distances between all particles

    # calculating pairwise gravitational forces using Newtons Law of Gravitation F = (G*mi*mj)/r^2
    fg = np.zeros_like(position)
    for i in range(NumParticles):  # for i particles
        for j in range(i + 1, NumParticles):  # for j particles
            F = G * mass[i] * mass[j] / dr[i][j] ** 2
            fg[i] += F * (position[j] - position[i]) / dr[i][j]
            fg[j] += -F * (position[j] - position[i]) / dr[i][j]

    # this updates the acceleration, velocity, and position of each particle
    acceleration = fg / mass[:, np.newaxis]
    velocity += acceleration * dt
    position += velocity * dt


plt.show()