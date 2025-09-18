import pygame
from random import uniform, choice

class PerlinNoise:
    def __init__(self, W, scale):
        self.n = W // scale + 1
        self.grid = [i for i in range(self.n)]
        self.grads = [uniform(-1, 1) for _ in range(self.n)]
        # self.grads = [choice((-1, 1)) for _ in range(self.n)]

    def fade(self, t):
        return t**3 * (t * (t * 6 - 15) + 10)

    def perlin_noise(self, x):
        lower = int(x)
        higher = lower + 1
        if higher >= self.n: return self.grads[lower]
        disp = [x - self.grid[lower], self.grid[higher] - x]
        dot = [self.grads[lower] * disp[0], self.grads[higher] * disp[1]]
        t = (x - self.grid[lower]) / (self.grid[higher] - self.grid[lower])
        t_faded = self.fade(t)
        val = dot[0] * (1 - t_faded) + dot[1] * t_faded
        return (val + 1) / 2

# Initialize pygame
pygame.init()

# Set up the window dimensions and scale
width, height = 800, 200
scale = 200  # The scale of the grid
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("1D Perlin Noise Visualization")

# Initialize PerlinNoise
perlin = PerlinNoise(W=width, scale=scale)

def interpolate_color(r, g, b, noise, rr, gg, bb):
    max_col = 255
    min_col = 0
    blended_r = int(r + (rr - r) * noise)
    blended_g = int(g + (gg - g) * noise)
    blended_b = int(b + (bb - b) * noise)
    blended_r = max(min(blended_r, max_col), min_col)
    blended_g = max(min(blended_g, max_col), min_col)
    blended_b = max(min(blended_b, max_col), min_col)
    return (blended_r, blended_g, blended_b)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the Perlin noise values across the screen
    for x in range(width):
        noise_value = perlin.perlin_noise(x / scale)  # x/scale to zoom in/out
        color = interpolate_color(0, 255, 255, noise_value, 255, 0, 0)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    pygame.display.flip()  # Update the display

# Quit pygame
pygame.quit()
