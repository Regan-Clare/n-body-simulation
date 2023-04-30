import numpy as np
from mayavi import mlab
import math


G = 6.67e-11
dt = 0.1


class BarnesHutTree:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.mass = 0
        self.center_of_mass = np.zeros(3)
        self.bodies = []
        self.children = []

    def insert(self, body):
        if not self.children:
            self.bodies.append(body)
            self.mass += body.mass
            self.center_of_mass += body.mass * body.pos
            if len(self.bodies) > 1:
                self.subdivide()
        else:
            idx = self.get_child_idx(body.pos)
            self.children[idx].insert(body)
            self.mass += body.mass
            self.center_of_mass += body.mass * body.pos

    def subdivide(self):
        child_size = self.size / 2
        for i in range(8):
            child_pos = self.pos + np.array([
                (i & 4) * child_size,
                (i & 2) * child_size,
                (i & 1) * child_size,
            ])
            self.children.append(BarnesHutTree(child_pos, child_size))
        for body in self.bodies:
            idx = self.get_child_idx(body.pos)
            self.children[idx].insert(body)
        self.bodies = []

    def get_child_idx(self, pos):
        idx = 0
        if pos[0] > self.pos[0] + self.size / 2:
            idx |= 4
        if pos[1] > self.pos[1] + self.size / 2:
            idx |= 2
        if pos[2] > self.pos[2] + self.size / 2:
            idx |= 1
        return idx

    def calculate_force(self, body, theta):
        if self.children:
            if self.size / np.linalg.norm(body.pos - self.center_of_mass) < theta:
                force = self.mass * (self.center_of_mass - body.pos) / np.linalg.norm(self.center_of_mass - body.pos) ** 3
                return force
            else:
                force = np.zeros(3)
                for child in self.children:
                    force += child.calculate_force(body, theta)
                return force
        else:
            if body in self.bodies:
                force = np.zeros(3)
                for other_body in self.bodies:
                    if other_body is not body:
                        r = other_body.pos - body.pos
                        force += G * body.mass * other_body.mass * r / np.linalg.norm(r) ** 3
                return force

class Body:
    def __init__(self, pos, vel, mass):
        self.pos = pos
        self.vel = vel
        self.mass = mass

def simulate(num_bodies, num_timesteps, theta):
    # Initialize the bodies
    bodies = []
    for i in range(num_bodies):
        pos = np.random.randn(3)
        vel = np.zeros(3)
        mass = np.random.rand() * 10
        bodies.append(Body(pos, vel, mass))

    # Build the Barnes-Hut tree
    tree = BarnesHutTree(np.zeros(3), 100)
    for body in bodies:
        tree.insert(body)

    # Simulate the motion
    for i in range(num_timesteps):
        # Calculate the forces on each body
        for body in bodies:
            force = tree.calculate_force(body, theta)
            body.vel += force / body.mass * dt
            body.pos += body.vel * dt

        # Rebuild the Barnes-Hut tree
        tree = BarnesHutTree(np.zeros(3), 100)
        for body in bodies:
            tree.insert(body)

            # Visualize the current state of the simulation
            fig = mlab.figure()
            x = [body.pos[0] for body in bodies]
            y = [body.pos[1] for body in bodies]
            z = [body.pos[2] for body in bodies]
            mlab.points3d(x, y, z, scale_factor=0.1)
            mlab.show()

            mlab.close()

    # Show the final state of the simulation
    fig = mlab.figure()
    x = [body.pos[0] for body in bodies]
    y = [body.pos[1] for body in bodies]
    z = [body.pos[2] for body in bodies]
    mlab.points3d(x, y, z, scale_factor=0.1)
    mlab.show()
    mlab.close()

