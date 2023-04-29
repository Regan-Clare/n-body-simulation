import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles
from matplotlib.widgets import Button  # allows me to use button widgets
from matplotlib.widgets import TextBox  # allows me to use text widgets
from mpl_toolkits.mplot3d import Axes3D


# SECTION 1 - INITIAL CONDITIONS AND CANVAS


# defining initial conditions
numParticles = int(input("How many particles in this system?: "))
m = 2  # mass
dt = 0.01  # this is the time step. dt meaning change in time.

# fixing value errors for start of simulation
while numParticles < 1:
    try:
        numParticles = int(input("How many particles in this system?: "))
        if numParticles < 1:
            print("Number of particles must be greater than or equal to 1. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# position and velocity variables - low/high is the range for which the values are randomised
x = np.random.uniform(low=0.5, high=10.5, size=numParticles)  # initial positions [x]... range 0.5 - 10.5
y = np.random.uniform(low=0.5, high=10.5, size=numParticles)  # initial positions [y]... range 0.5 - 10.5
z = np.random.uniform(low=0.5, high=10.5, size=numParticles)  # initial positions [z]... range 0.5 - 10.5
vx = np.random.uniform(low=0, high=0.5, size=numParticles)  # initial x-velocity... range 0 - 0.2
vy = np.random.uniform(low=0, high=0.5, size=numParticles)  # initial y-velocity... range 0 - 0.2
vz = np.random.uniform(low=0, high=0.5, size=numParticles)  # initial z-velocity... range 0 - 0.2

cx = [[] for _ in range(numParticles)]  # new positions for x-value on particles
cy = [[] for _ in range(numParticles)]  # new positions for y-value on particles
cz = [[] for _ in range(numParticles)]  # new positions for z-value on particles

# CANVAS

# create a 3D figure
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# set the background color to grey
ax.set_facecolor('grey')

# remove grid lines
ax.grid(False)

# remove x, y, z labels
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])

# remove axis ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# customize the plot
ax.set_xlim(0, 11)
ax.set_ylim(0, 11)
ax.set_zlim(0, 11)

ax.set_title('3D N-Body Simulation')


# BUTTONS AND UI


# variable for zooming in and out of graph
zoom = 1.0


def on_scroll(event):
    global zoom
    if event.button == 'up':  # if scroll wheel is moved up...
        zoom -= 0.1  # then subtract 0.1 to the zoom, making the zoom smaller

    elif event.button == 'down':  # if scroll wheel is moved down...
        zoom += 0.1  # then add 0.1 to the zoom, making the zoom larger

    ax.set_box_aspect(None, zoom=zoom)  # update the zoom in here
    fig.canvas.draw()  # update on canvas


fig.canvas.mpl_connect('scroll_event', on_scroll)

# FUNCTIONS AND CALCULATIONS


# trail line function
def lines():
    global lineList, scatterList, line, cy, cx, cz
    lineList = []  # empty list for plotting line positions
    scatterList = []  # empty list for plotting positions
    for i in range(numParticles):
        cx[i] = []  # empty list for x-position of line for ith particle
        cy[i] = []  # empty list for y-position of line for ith particle
        cz[i] = []  # empty list for x-position of line for ith particle

        rand_colour = np.random.rand(3)  # RGB RNG between 0 and 1 three times. So lines and particles are same colour
        faded_colour = tuple(np.append(rand_colour, 0.6))  # rgba, a = alpha value => translucent

        scatter, = ax.plot([], [], [], 'o', markersize=5, color=rand_colour)  # plots the particles on the graph
        scatter.set_zorder(3)  # brings particles to the front, in front of lines
        scatterList.append(scatter)  # appends the scatter values to the scatter list

        line, = ax.plot([], [], '-', color=faded_colour)  # plots the trail lines on the graph
        lineList.append(line)  # appends the line values to the line list


lines()


# initial conditions
def initial_conditions():
    for i in range(numParticles):
        lineList[i].set_data_3d(cx[i], cy[i], cz[i])  # setting x, y data corresponding to the ith particle in initial position
        scatterList[i].set_data_3d([x[i]], [y[i]], [z[i]])

    return scatterList + [line]


initial_conditions()


softeningLength = 0.2  # softening for collisions to mitigate unrealistic collisions


# updating parameters
def update(frame):
    global x, y, z, vx, vy, vz, r, cx, cy, cz
    r = 0  # this is just so r is initialized before the nested for loop

    for i in range(numParticles):
        for j in range(i + 1, numParticles):
            dx = x[j] - x[i]  # calculates difference of x-position of jth particle to x-position of ith particle
            dy = y[j] - y[i]  # calculates difference of y-position of jth particle to y-position of ith particle
            dz = z[j] - z[i]  # calculates difference of z-position of jth particle to z-position of ith particle

            r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)  # pair-wise distance between two objects, calculated using pythagoras
            # check for collision
            if r < softeningLength:  # if the radius is less than 0.1...
                r = softeningLength  # set it to 0.1

            fx = m * dx / (r ** 3)  # x-component of the force between 'i' and 'j'
            fy = m * dy / (r ** 3)  # y-component of the force between 'i' and 'j'
            fz = m * dz / (r ** 3)  # z-component of the force between 'i' and 'j'

            vx[i] += dt * fx  # updating the x-velocity of ith particle
            vy[i] += dt * fy  # updating the y-velocity of ith particle
            vz[i] += dt * fz  # updating the z-velocity of ith particle
            vx[j] -= dt * fx  # updating the x-velocity of jth particle
            vy[j] -= dt * fy  # updating the y-velocity of jth particle
            vz[j] -= dt * fz  # updating the z-velocity of jth particle

        x[i] += dt * vx[i]  # updating x-position based on its velocity, over time
        y[i] += dt * vy[i]  # updating y-position based on its velocity, over time
        z[i] += dt * vz[i]  # updating z-position based on its velocity, over time

        cx[i].append(x[i])  # store new/ positions to list of previous positions (this is for line)
        cy[i].append(y[i])  # store new/ positions to list of previous positions (this is for line)
        cz[i].append(z[i])  # store new/ positions to list of previous positions (this is for line)

        scatterList[i].set_data_3d([x[i]], [y[i]], [z[i]])  # updating xyz on scatter plot for the ith particle
        lineList[i].set_data_3d(cx[i], cy[i], cz[i])  # updating xyz for lines that follow ith particle

    for i in range(numParticles):
        line.set_data_3d(cx[i], cy[i], cz[i])  # plot curve for each particle

    return scatterList + [line] + lineList


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=False, save_count=9000)

plt.show()
