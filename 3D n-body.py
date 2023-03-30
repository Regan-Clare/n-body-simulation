import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim  # allows for animating the particles

# Define constants
G = 6.674e-11  # Gravitational constant
dt = 0.01  # Time step

# Define initial conditions
m = np.array([1, 1, 1])  # Masses
r = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float64)  # Positions
v = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64)  # Velocities


# Define acceleration function
def acceleration(r, m):
    n = len(r)
    a = np.zeros((n, 3))
    for i in range(n):
        for j in range(n):
            if i != j:
                rij = r[j] - r[i]
                a[i] += G * m[j] * rij / np.linalg.norm(rij) ** 3
    return a


# Initialize arrays for plotting
rs = [r]
vs = [v]

# Run simulation
t = 0
t_end = 10
while t < t_end:
    # Update positions and velocities
    a = acceleration(r, m)
    r += (v * dt).astype(r.dtype)
    v += (a * dt).astype(v.dtype)

    # Store positions and velocities for plotting
    rs.append(r)
    vs.append(v)

    # Update time
    t += dt


def init():
    for line in lines:
        line.set_data_3d([], [], [])
    for pt in pts:
        pt.set_data_3d([], [], [])
    return lines + pts


# Define animation update function
# Define animation update function
def update(num, lines, pts):
    global r, v, a
    # Update positions and velocities
    a = acceleration(r, m)
    r += (v * dt).astype(r.dtype)
    v += (a * dt).astype(v.dtype)

    # Update particle positions
    for i, line in enumerate(lines):
        line.set_data_3d(rs[num][:, i, 0], rs[num][:, i, 1], rs[num][:, i, 2])

    # Update particle trajectories
    for i, pt in enumerate(pts):
        pt.set_data_3d(rs[:num, i, 0], rs[:num, i, 1], rs[:num, i, 2])

    return lines + pts



# Convert position and velocity lists to numpy arrays
rs = np.array(rs)
vs = np.array(vs)

# Plot trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(len(m)):
    ax.plot(rs[:, i, 0], rs[:, i, 1], rs[:, i, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])

# Initialize particle positions and trajectories
lines = [ax.plot([], [], [], '-')[0] for i in range(len(m))]
pts = [ax.plot([], [], [], '.', markersize=5)[0] for i in range(len(m))]

ax.scatter(r[:, 0], r[:, 1], r[:, 2], s=75, c=['red', 'green', 'blue'])

anim_obj = anim.FuncAnimation(fig, update, init_func=init, frames=len(rs), fargs=(lines, pts), interval=10)

plt.show()

