import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points

# defining initial conditions
NumParticles = int(input("How many particles in this system?: "))
m = 5  # 5.972e24 Earth's Mass
dt = 0.01  # this is the time step. dt meaning change in time.


x = np.random.uniform(low=0.2, high=9.8, size=NumParticles)  # initial positions [x]
y = np.random.uniform(low=0.2, high=9.8, size=NumParticles)  # initial positions [y]
vx = np.random.uniform(low=0, high=0.3, size=NumParticles)  # initial x-velocity
vy = np.random.uniform(low=0, high=0.3, size=NumParticles)  # initial y-velocity

cx = [[] for _ in range(NumParticles)]  # new positions for x-axis
cy = [[] for _ in range(NumParticles)]  # new positions for y-axis

scatter_list = []

for i in range(NumParticles):
    cx[i] = []
    cy[i] = []
    scatter, = ax.plot([], [], 'o', markersize=5, color='black')
    scatter_list.append(scatter)

line, = ax.plot([], [], '-', color='blue')


def initial_conditions():
    for i in range(NumParticles):
        scatter_list[i].set_data(x[i], y[i])

    line.set_data([], [])

    return scatter_list + [line]


initial_conditions()


def update(frame):
    global x, y, vx, vy, r, cx, cy
    r = 0  # this is just so r is initialized before the nested for loop

    for i in range(NumParticles):
        for j in range(i + 1, NumParticles):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            r = np.sqrt(dx ** 2 + dy ** 2)
            fx = m * dx / (r ** 3)
            fy = m * dy / (r ** 3)
            vx[i] += dt * fx
            vy[i] += dt * fy
            vx[j] -= dt * fx
            vy[j] -= dt * fy
        x[i] += dt * vx[i]
        y[i] += dt * vy[i]
        cx[i].append(x[i])  # store new/previous positions - doesn't matter
        cy[i].append(y[i])  # store new/previous positions - doesn't matter
        scatter_list[i].set_data(x[i], y[i])

    for i in range(NumParticles):
        line.set_data(cx[i], cy[i])  # plot curve for each particle

    return scatter_list + [line]


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=True, save_count=9000)

plt.show()