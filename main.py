import pygame
from pygame import Vector2 as V2
import random
from math import cos, sin, pi

pygame.init()

def perlin_noise(given: V2, grid_scale, seed=12345) -> float:
    def get_gradient(x, y):
        random.seed(x * seed**2 + y * seed + seed)
        angle = random.uniform(0, 2 * pi)
        return V2(cos(angle), sin(angle))
    
    t_fade = lambda t: (t**3) * (t * (6 * t - 15) + 10)  # Smooth fade function

    # noramlise (sorta) the given (aka make it a float)
    if isinstance(grid_scale, V2): given = V2(given.x/grid_scale.x, given.y/grid_scale.y)
    else: given /= grid_scale
    
    # Grid cell corners
    bl = V2(int(given.x), int(given.y))
    br = bl + V2(1, 0)
    tl = bl + V2(0, 1)
    tr = bl + V2(1, 1)

    # Gradients at each corner
    grads_bl = get_gradient(bl.x, bl.y)
    grads_br = get_gradient(br.x, br.y)
    grads_tl = get_gradient(tl.x, tl.y)
    grads_tr = get_gradient(tr.x, tr.y)
    
    # Displacement vectors
    disp_bl = given - bl
    disp_br = given - br
    disp_tl = given - tl
    disp_tr = given - tr

    # Dot products
    dot_bl = grads_bl.dot(disp_bl)
    dot_br = grads_br.dot(disp_br)
    dot_tl = grads_tl.dot(disp_tl)
    dot_tr = grads_tr.dot(disp_tr)
    
    # Fade values
    tx = (given.x - bl.x) / (br.x - bl.x)
    if (tr.y == tl.y): ty = (given.y - bl.y)    
    else: ty = ((given.y - tl.y) / (tr.y - tl.y))
    
    tx = t_fade(tx)
    ty = t_fade(ty)
    
    # Interpolation
    inter_x1 = (1 - tx) * dot_bl + tx * dot_br
    inter_x2 = (1 - tx) * dot_tl + tx * dot_tr
    final_val = (1 - ty) * inter_x1 + ty * inter_x2
    
    return (final_val + 1) / 2

# Pygame setup
RES = W,H = 800,600
screen = pygame.display.set_mode(RES)

# Generate Perlin noise
for x in range(0, W):
    for y in range(0, H):
        noise = perlin_noise(V2(x, y), grid_scale = V2(8,6), seed=1337)  # Adjust scaling for smoother transitions
        color = [int(noise * 255)] * 3  # Grayscale color
        screen.set_at((x, y), color)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    pygame.display.flip()

pygame.quit()
