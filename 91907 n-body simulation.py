import numpy as np  # this library is used for linear algebra. I.e. matrix algebra
import matplotlib.pyplot as plt  # use for plotting data on a canvas
import matplotlib.animation as anim  # allows for animating the particles
from matplotlib.widgets import Button  # allows me to use button widgets
from matplotlib.widgets import TextBox  # allows me to use text widgets


# I am writing variables in lowerCamelCase and functions in snake_case


# defining initial conditions
numParticles = int(input("How many particles in this system?: "))  # number of particles in the system
m = 2  # Mass
dt = 0.005  # this is the time step. dt meaning change in time.


# position and velocity variables - low/high is the range for which the values are randomised
x = np.random.uniform(low=0.2, high=9.8, size=numParticles)  # initial positions [x]
y = np.random.uniform(low=0.2, high=9.8, size=numParticles)  # initial positions [y]
vx = np.random.uniform(low=0, high=0.2, size=numParticles)  # initial x-velocity
vy = np.random.uniform(low=0, high=0.2, size=numParticles)  # initial y-velocity

cx = [[] for _ in range(numParticles)]  # new positions for x-axis
cy = [[] for _ in range(numParticles)]  # new positions for y-axis


# CANVAS
fig = plt.figure(figsize=(10, 10))  # the size of the canvas
ax = plt.axes(xlim=(0, 10), ylim=(0, 10))  # the size of the axis points


# NUMBER OF PARTICLES DISPLAY
plt.title("{}-body Simulation".format(numParticles))  # title for simulation
plt.xlabel("Astronomical Unit (AU)")  # x-label
plt.ylabel("Astronomical Unit (AU)")  # y-label


# PAUSE BUTTON
animationStop = False


def on_pause(event):
    global animationStop, pauseButton
    animationStop = not animationStop  # toggles boolean value every time button is clicked False <=> True
    if animationStop:
        pauseButton.label.set_text('Resume')  # if animation false, set text to 'Resume'
    else:
        pauseButton.label.set_text('Pause')  # if animation true, set text to 'Pause'


pauseButtonPos = plt.axes([0.8, 0.9, 0.1, 0.1])  # position of pause button
pauseButton = Button(pauseButtonPos, 'Pause', color='white', hovercolor='grey')  # conditions of pause button
pauseButton.on_clicked(on_pause)  # when button is clicked, run onPause function


# REPLAY BUTTON
# I came up with the idea that I'd need to save the initial conditions in a list, then access them for the reset
initialConditionsLog = []


def save_initial_conditions():  # saving initial conditions by using appending the values into the list above
    # positions and velocities are appended to the list
    initialConditionsLog.append((np.copy(x), np.copy(y), np.copy(vx), np.copy(vy)))


save_initial_conditions()


def replay_simulation(event):
    global x, y, vx, vy
    x, y, vx, vy = initialConditionsLog[-1]  # -1 accesses the last set of initial conditions in the log, reverse order
    for i in range(numParticles):
        cx[i] = []  # clearing the lists for new positions
        cy[i] = []
    initial_conditions()  # replay the initial conditions
    save_initial_conditions()  # save the new initial conditions after resetting the simulation
    return scatterList + lineList


replayButtonPos = plt.axes([0.125, 0.9, 0.1, 0.1])  # position of replay function
replayButton = Button(replayButtonPos, 'Replay', color='white', hovercolor='grey')  # conditions for replay button
replayButton.on_clicked(replay_simulation)  # when replay button is clicked, run replay function


# Change Number of Particles
def change_num_particles(num):
    global numParticles, x, y, vx, vy
    try:
        numParticles = int(num)
    except ValueError:
        print("Error: Input value is not a valid integer")
        return
    initialConditionsLog.clear()
    save_initial_conditions()
    return scatterList + lineList


particleTextPos = plt.axes([0.58, 0.95, 0.05, 0.05])  # position of replay function
particleText = TextBox(particleTextPos, 'Change Number of Bodies to:', color='white', hovercolor='grey')  # conditions for particle text
particleText.on_submit(lambda text: change_num_particles(text))


# LISTS
lineList = []  # empty list for plotting line positions
scatterList = []  # empty list for plotting positions
for i in range(numParticles):
    cx[i] = []  # empty list for x-position of line for ith particle
    cy[i] = []  # empty list for y-position of line for ith particle
    scatter, = ax.plot([], [], 'o', markersize=4, color='black')  # plots the particles on the graph
    # z-order determines the order in which different elements are drawn, since 3 > z-order of lines, particles in front
    # short for z-axis-order
    scatter.set_zorder(3)  # brings particles to the front, in front of lines
    scatterList.append(scatter)  # appends the scatter values to the scatter list
    line, = ax.plot([], [], '-', color='purple')  # plots the trail lines on the graph
    lineList.append(line)  # appends the line values to the line list


def initial_conditions():
    for i in range(numParticles):
        lineList[i].set_data(cx[i], cy[i])  # setting x, y data corresponding to the ith particle in initial position
        scatterList[i].set_data(x[i], y[i])  # setting x, y data corresponding to the ith particle in initial position

    return scatterList + [line]


initial_conditions()


softening_length = 0.2  # softening for collisions to mitigate unrealistic collisions


def update(frame):
    global x, y, vx, vy, r, cx, cy, animationStop
    r = 0  # this is just so r is initialized before the nested for loop
    if animationStop:
        # If animation is paused, return current state of the scatter and line objects without updating their positions
        return scatterList + lineList

    for i in range(numParticles):
        for j in range(i + 1, numParticles):
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
        scatterList[i].set_data(x[i], y[i])  # updating x and y on scatter plot for the ith particle
        lineList[i].set_data(cx[i], cy[i])  # updating x and y for lines that follow ith particle

    for i in range(numParticles):
        line.set_data(cx[i], cy[i])  # plot curve for each particle

    return scatterList + [line] + lineList


ani = anim.FuncAnimation(fig, update, init_func=initial_conditions, interval=1, blit=True, save_count=9000)


plt.show()
