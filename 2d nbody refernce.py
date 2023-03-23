import matplotlib.pyplot as plt
import matplotlib.animation as anim

fig = plt.figure(figsize=(6, 6))
ax = plt.axes(xlim=(-1, 1), ylim=(-1, 1))
#R,G,B
x = [-0.4, 0.4, 0]  # x-positioning
y = [0, 0, 0]  # y-positioning
dx = [0, 0, 0]  # initial x-velocity
dy = [1, -1, 0.2]  # initial y-velocity
M = [2, 2]  # mass (molar mass?)
dt = 0.003  # time
cx = [[], [], []]
cy = [[], [], []]

curve1, = ax.plot([], [], 'r-')
curve2, = ax.plot([], [], 'g-')
curve3, = ax.plot([], [], 'b-')

obj1, = plt.plot([], [], 'ro')
obj2, = plt.plot([], [], 'go')
obj3, = plt.plot([], [], 'bo')


def init():
    curve1.set_data([], [])
    curve2.set_data([], [])
    curve3.set_data([], [])
    obj1.set_data([], [])
    obj2.set_data([], [])
    obj3.set_data([], [])
    return curve1, curve2, curve3, obj1, obj2, obj3,


def f(t):
    global x, y, dx, dy, r
    for i in range(2):
        j = (i + 1) % 2
        dx[i] += dt * M[j] * (x[j] - x[i]) / ((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2) ** 1.5
        dy[i] += dt * M[j] * (y[j] - y[i]) / ((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2) ** 1.5
        dx[2] += dt * M[i] * (x[i] - x[2]) / ((x[i] - x[2]) ** 2 + (y[i] - y[2]) ** 2) ** 1.5
        dy[2] += dt * M[i] * (y[i] - y[2]) / ((x[i] - x[2]) ** 2 + (y[i] - y[2]) ** 2) ** 1.5
    for i in range(3):
        x[i] += dt * dx[i]
        y[i] += dt * dy[i]
        cx[i].append(x[i])
        cy[i].append(y[i])
    curve1.set_data(cx[0], cy[0])
    curve2.set_data(cx[1], cy[1])
    curve3.set_data(cx[2], cy[2])
    obj1.set_data(x[0], y[0])
    obj2.set_data(x[1], y[1])
    obj3.set_data(x[2], y[2])
    return curve1, curve2, curve3, obj1, obj2, obj3,


meh = anim.FuncAnimation(fig, f, init_func=init, interval=1, blit=True, save_count=(9000))
plt.show()