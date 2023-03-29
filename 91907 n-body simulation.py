import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points

# defining initial conditions
NumParticles = int(input("How many particles in this system?: "))
m = 2  # 5.972e24 Earth's Mass
dt = 0.1  # this is the time step. dt meaning change in time.


x = np.random.uniform(low=0.2, high=9.8, size=NumParticles) # initial positions [x]
y = np.random.uniform(low=0.2, high=9.8, size=NumParticles)  # initial positions [y]
vx = np.random.uniform(low=0, high=0.1, size=NumParticles)  # initial x-velocity
vy = np.random.uniform(low=0, high=0.1, size=NumParticles)  # initial y-velocity

cx = [[] for _ in range(NumParticles)]  # new positions for x-axis
cy = [[] for _ in range(NumParticles)]  # new positions for y-axis

curve, = ax.plot([], [])
obj, = plt.plot([], [])


def initial_conditions():
    curve.set_data([], [])
    obj.set_data([], [])
    # here, scatter is a method to plot objects and uses ax as a reference frame
    # this means that when 'i' is the number of particles, then...
    # the scatter method plots the position, size (s), and colour of the particles on the canvas
    # the [i, 0] and [i, 1] extract the x and y coordinates of the i-th particle respectively.
    # 0 being the first column x, and 1 being the second column y
    # these basically refer back to the matrices/arrays I made earlier
    for i in range(NumParticles):
        ax.scatter(x, y, s=40, c='black')  # x-position, y-position, size, colour
    return curve, obj,


initial_conditions()


def update(frame):
    global x, y, vx, vy, r
    for i in range(NumParticles):
        for j in range(i + 1, NumParticles):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            r = np.sqrt(dx ** 2 + dy ** 2)
            fx = m * dx / (r ** 3)
            fy = m * dy / (r ** 3)
            x[i] += dt * fx
            y[i] += dt * fy
            x[j] -= dt * fx
            y[j] -= dt * fy
        x[i] += dt * vx[i]
        y[i] += dt * vy[i]
        cx[i].append(x[i])
        cy[i].append(y[i])
    curve.set_data(cx, cy)
    obj.set_data(x, y)

    return curve, obj,


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=True, save_count=9000)

plt.show()