import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

n = int(input("Enter the size of the Grid "))
k = int(input("Enter the number of particle "))
if k > n**2 :
    raise ValueError("Number particles is more than the size of the grid")
stickiness = float(input("Enter stickiness. Should be between 0 and 1 "))
if not (0 <= stickiness <= 1):
    raise ValueError("Out of range")
steps = 5000
moves = np.array([[1,0], [-1,0], [0,1], [0,-1]], dtype=int)
grid = np.zeros((n,n), dtype=int)

grid[n//2, n//2] = 1
cluster =1

def check_neighbour(pos):
    (i,j) = pos
    for di, dj in moves:
        ni, nj = (i + di) % n, (j + dj) % n

        if grid[ni,nj] == 1:
            return True
        
    return False

def random_cell():
    empty = np.argwhere(grid == 0)
    occupied = np.argwhere(grid == 1)
    if len(empty) == 0:
        return None
    
    particle =[]
    for em in empty:
        distances = [distance(em, oc) for oc in occupied]
        if min(distances)>= 4:
            particle.append(em)
    if len(particle) ==0:
        return None
    i = np.random.randint(len(particle))
    return tuple(particle[i])

def distance(pos1, pos2):
    dy = min(abs(pos1[0]-pos2[0]), n - abs(pos1[0]-pos2[0]))
    dx = min(abs(pos1[1]-pos2[1]), n - abs(pos1[1]-pos2[1]))
    return np.sqrt(dx**2 + dy**2)

def random_walk():
    global cluster
    pos = random_cell()
    if pos is None:
        return
    x, y = pos
    for _ in range(steps):
        if check_neighbour((x,y)):
            if np.random.rand() < stickiness:
                grid[x,y] = 1
                cluster+=1
                return
        dx, dy = moves[np.random.randint(4)]
        x, y = (x + dx) % n, (y + dy) % n



fig, ax = plt.subplots(figsize=(5,5))
im = ax.imshow(grid, cmap='gray_r', vmin=0, vmax=1, interpolation='nearest')
ax.axis('off')


def anim(frame):
    random_walk()
    im.set_data(grid)

    return [im]

ani = FuncAnimation(fig, anim, frames=k, interval=1, blit=True)
plt.show()


    


