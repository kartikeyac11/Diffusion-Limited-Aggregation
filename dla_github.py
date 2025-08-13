import matplotlib
matplotlib.use('TkAgg')  # ensures real-time pop-up works in VS Code

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
N = 15
K = 150
stickiness = 1
max_steps = 100000
moves = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=int)

grid = np.zeros((N, N), dtype=np.uint8)
center = (N // 2, N // 2)
grid[center] = 1

def has_occupied_neighbor(pos):
    i, j = pos
    for di, dj in moves:
        ni, nj = i + di, j + dj
        if 0 <= ni < N and 0 <= nj < N and grid[ni, nj] == 1:
            return True
    return False

def get_cluster_radius():
    ys, xs = np.where(grid == 1)
    if len(xs) == 0:
        return 0
    dx = xs - center[1]
    dy = ys - center[0]
    return int(np.max(np.sqrt(dx**2 + dy**2)))

def spawn_particle():
    """Spawn particle on a random empty boundary cell."""
    while True:
        side = np.random.randint(4)
        if side == 0:       # top row
            pos = np.array([0, np.random.randint(N)], dtype=int)
        elif side == 1:     # bottom row
            pos = np.array([N - 1, np.random.randint(N)], dtype=int)
        elif side == 2:     # left column
            pos = np.array([np.random.randint(N), 0], dtype=int)
        else:               # right column
            pos = np.array([np.random.randint(N), N - 1], dtype=int)

        if grid[tuple(pos)] == 0:  # only if empty
            return pos

def random_walk_until_stick():
    pos = spawn_particle()
    R_kill = N//2 - 1
    for _ in range(max_steps):
        if has_occupied_neighbor(pos):
            if np.random.rand() < stickiness:
                grid[tuple(pos)] = 1
                return
        step = moves[np.random.randint(4)]
        pos = pos + step
        dy, dx = pos[0] - center[0], pos[1] - center[1]
        if np.sqrt(dx**2 + dy**2) > R_kill:
            return

# Animation setup
fig, ax = plt.subplots(figsize=(5,5))
im = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1, interpolation='nearest')
ax.axis('off')

def update(frame):
    random_walk_until_stick()
    im.set_data(grid)
    return [im]

ani = FuncAnimation(fig, update, frames=K, interval=1, blit=True)

plt.show()
