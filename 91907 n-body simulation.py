import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles

# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points


# defining initial conditions
NumParticles = int(input("How many particles in this system?: "))
m = 2  # 5.972e24 Earth's Mass
dt = 0.005  # this is the time step. dt meaning change in time.


x = np.random.uniform(low=0.2, high=9.8, size=NumParticles)  # initial positions [x]
y = np.random.uniform(low=0.2, high=9.8, size=NumParticles)  # initial positions [y]
vx = np.random.uniform(low=0, high=0.2, size=NumParticles)  # initial x-velocity
vy = np.random.uniform(low=0, high=0.2, size=NumParticles)  # initial y-velocity

cx = [[] for _ in range(NumParticles)]  # new positions for x-axis
cy = [[] for _ in range(NumParticles)]  # new positions for y-axis

scatter_list = []  # empty list for plotting positions
line_list = []  # empty list for plotting line positions
for i in range(NumParticles):
    cx[i] = []  # empty list for x-position of line for ith particle
    cy[i] = []  # empty list for y-position of line for ith particle
    scatter, = ax.plot([], [], 'o', markersize=4, color='black')  # plots the particles on the graph
    scatter_list.append(scatter)  # appends the scatter values to the scatter list
    line, = ax.plot([], [], '-', color='purple')  # plots the trail lines on the graph
    line_list.append(line)  # appends the line values to the line list


def initial_conditions():
    for i in range(NumParticles):
        scatter_list[i].set_data(x[i], y[i])  # setting x, y data corresponding to the ith particle in initial position
        line_list[i].set_data(cx[i], cy[i])  # setting x, y data corresponding to the ith particle in initial position

    return scatter_list + [line]


initial_conditions()


softening_length = 0.2  # softening for collisions to mitigate unrealistic collisions

def update(frame):
    global x, y, vx, vy, r, cx, cy
    r = 0  # this is just so r is initialized before the nested for loop

    for i in range(NumParticles):
        for j in range(i + 1, NumParticles):
            dx = x[j] - x[i]  # calculates difference of x-position of jth particle to x-position of ith particle
            dy = y[j] - y[i]  # calculates difference of y-position of jth particle to y-position of ith particle
            r = np.sqrt(dx ** 2 + dy ** 2)  # pair-wise distance between two objects, calculated using pythagoras
            # check for collision
            if r < softening_length:  # if the radius is less than 0.1...
                r = softening_length  # set it to 0.1

            fx = m * dx / (r ** 3)  # x-component of the force between 'i' and 'j'
            fy = m * dy / (r ** 3)  # y-component of the force between 'i' and 'j'
            vx[i] += dt * fx  # updating the x-velocity of ith particle
            vy[i] += dt * fy  # updating the y-velocity of ith particle
            vx[j] -= dt * fx  # updating the x-velocity of jth particle
            vy[j] -= dt * fy  # updating the y-velocity of jth particle
        x[i] += dt * vx[i]  # updating x-position based on its velocity, over time
        y[i] += dt * vy[i]  # updating y-position based on its velocity, over time
        cx[i].append(x[i])  # store new/ positions to list of previous positions (this is for line)
        cy[i].append(y[i])  # store new/ positions to list of previous positions (this is for line)
        scatter_list[i].set_data(x[i], y[i])  # updating x and y on scatter plot for the ith particle
        line_list[i].set_data(cx[i], cy[i])  # updating x and y for lines that follow ith particle

    for i in range(NumParticles):
        line.set_data(cx[i], cy[i])  # plot curve for each particle

    return scatter_list + [line] + line_list


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=True, save_count=9000)


plt.show()