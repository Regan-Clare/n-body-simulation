import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points


# defining initial conditions
EM = 5.972e24  # Earth's Mass
G = 6.6743e-11  # Gravitational constant
dt = 0.1  # this is the time step. dt meaning change in time.


def initial_conditions():
    global NumParticles, masses, nP, velocities, m
    NumParticles = int(input("How many particles in this system?: "))
    masses = []
    nP = []  # new position for x and y values
    velocities = []
    for i in range(NumParticles):
        m = float(input(f"Mass of particle {i+1}: "))
        masses.append(m)
        x = float(input(f"x-position of particle {i+1}: "))
        y = float(input(f"y-position of particle {i+1}: "))
        nP.append([x, y])
        vx = float(input(f"x-velocity of particle {i+1}: "))
        vy = float(input(f"y-velocity of particle {i+1}: "))
        velocities.append([vx, vy])


initial_conditions()



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
    ax.scatter(nP[0], nP[1], s=ParticleSizes[i], color=ParticleColours[i])


def update():
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
            F = G * m[i] * m[j] / dr[i][j] ** 2  # Newton's Universal Law of Gravitation
            fg[i] += F * (P[j] - P[i]) / dr[i][j]
            fg[j] += -F * (P[j] - P[i]) / dr[i][j]

    # this updates the acceleration, velocity, and position of each particle
    acceleration = fg / m[:, np.newaxis]  # F = ma (Newton's Second Law)
    v += acceleration * dt  # a = v/t => v = a*t
    P += v * dt  # position changes with respect to velocity over a change in time

    for i in range(NumParticles):  # this accounts for new position over time
        nP[i] += dt * P[i, 0]
        nP[i] += dt * P[i, 1]
        nP[i].append(P[i, 0])
        nP[i].append(P[i, 1])


plt.show()