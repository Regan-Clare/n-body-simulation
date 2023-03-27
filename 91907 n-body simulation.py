import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
from matplotlib.animation import FuncAnimation  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points

# defining initial conditions
EM = 5  # 5.972e24 Earth's Mass
G = 6.6743e-11  # Gravitational constant
dt = 0.1  # this is the time step. dt meaning change in time.
NumParticles = 2  # has to be >= 2 to avoid errors in pairwise calculations (dP and dv = (N, 2)

# initialize dP and dv with zeros
dP = np.zeros((NumParticles, 2))
dv = np.zeros((NumParticles, 2))

def initial_conditions():
    global NumParticles, m, P, v, dP, dv
    NumParticles = int(input("How many particles in this system?: "))
    try:  # this prevents non integers and values < 2 from being entered
        while True:
            if NumParticles < 2:
                initial_conditions()
            else:
                break
    except ValueError:
        initial_conditions()
    m = [EM] * NumParticles
    P = np.random.rand(NumParticles, 2) * 10  # initial positions
    v = np.zeros((NumParticles, 2))  # initial velocities
    dP = np.copy(P)  # initialize dP with the initial positions
    dv = np.copy(v)  # initialize dv with the initial velocities

    for i in range(NumParticles):
        x = np.random.uniform(0, 9.8)  # values at 9.8 so particles don't hit edge of system
        y = np.random.uniform(0, 9.8)
        P[i] = np.array([x, y])


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
    global dP  # change in position
    global dv  # change in velocity

    # calculate pairwise distances between particles, subtract.outer() computes out level of products for vectors/arrays
    dx = np.subtract.outer(dP[:, 0], dP[:, 0])  # difference of [i, j] for x input
    dy = np.subtract.outer(dP[:, 1], dP[:, 1])  # difference of [i, j] for y input
    dr = np.sqrt(dx ** 2 + dy ** 2)  # uses element-wise sqrt to return non-negative sqrt of an array for each element
    # it calculates the sum of the squares of the elements dy and dx, giving pairwise distances between all particles

    # calculating pairwise gravitational forces using Newtons Law of Gravitation F = (G*mi*mj)/r^2
    fg = np.zeros_like(dP)
    for i in range(NumParticles):  # for i particles
        for j in range(i + 1, NumParticles):  # for j particles
            F = G * m[i] * m[j] / dr[i][j] ** 2  # Newton's Universal Law of Gravitation
            fg[i] += F * (dP[j] - dP[i]) / dr[i][j]
            fg[j] += -F * (dP[j] - dP[i]) / dr[i][j]

    # this updates the acceleration, velocity, and position of each particle
    acceleration = fg / m[:, np.newaxis]  # F = ma (Newton's Second Law)
    dv += acceleration * dt  # a = v/t => v = a*t
    dP += v * dt  # position changes with respect to velocity over a change in time

    for i in range(NumParticles):
        P[i, 0] += dt * dP[i, 0]
        P[i, 1] += dt * dP[i, 1]


animation = FuncAnimation(fig, func=update, frames=np.arange(0, 10, 0.01), interval=50, blit=True)

plt.show()