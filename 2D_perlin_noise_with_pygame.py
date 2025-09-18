
'''
NOT AS FAST AS I WANTED
WILL TRY AGAIN LATER (the 2d part)

1d worked flawlessly
'''











import numpy as np
# import cupy as cp
import math
import random
from pygame import Vector2 as V2
import pygame
import pygame.surfarray as surfarray


class PerlinNoise:
    def __init__(self, width, height, scale_of_grid_cell: V2):
        self.width = width
        self.height = height
        self.scale_of_grid_cell = scale_of_grid_cell

        # Generate random gradients for each grid point
        self.grid = self._generate_grid(width, height)

    def _generate_grid(self, width, height):
        """Generates a grid of random gradients."""
        grid = np.zeros((width, height, 2))  # (x, y) gradient directions
        for i in range(width):
            for j in range(height):
                angle = random.uniform(0, 2 * math.pi)
                grid[i, j] = np.array([math.cos(angle), math.sin(angle)])
        return grid

    def _dot_product(self, grid_point, pos):
        """Calculate dot product between gradient vector and distance vector."""
        gradient = self.grid[grid_point[0], grid_point[1]]
        distance = pos - np.array([grid_point[0], grid_point[1]])  # pos is now a numpy array
        return np.dot(gradient, distance)

    def _smoothstep(self, t):
        """Smooth interpolation (smoothstep function)."""
        return t * t * (3 - 2 * t)

    def _get_value_at_grid_point(self, pos):
        """Fetches the Perlin noise value at a specific position."""
        # Scale position to the grid scale
        pos_scaled = np.array([pos[0] / self.scale_of_grid_cell.x, pos[1] / self.scale_of_grid_cell.y])

        # Get the integer grid coordinates
        x0, y0 = np.floor(pos_scaled).astype(int)
        x1, y1 = x0 + 1, y0 + 1

        # Get the local position inside the grid square (0-1)
        sx = pos_scaled[0] - x0
        sy = pos_scaled[1] - y0

        # Compute the fade function
        sx = self._smoothstep(sx)
        sy = self._smoothstep(sy)

        # Dot product at the 4 corners
        n00 = self._dot_product((x0, y0), pos_scaled)
        n01 = self._dot_product((x0, y1), pos_scaled)
        n10 = self._dot_product((x1, y0), pos_scaled)
        n11 = self._dot_product((x1, y1), pos_scaled)

        # Interpolate the values
        ix0 = n00 + sx * (n10 - n00)
        ix1 = n01 + sx * (n11 - n01)
        value = ix0 + sy * (ix1 - ix0)

        # Normalize to [0, 1] by shifting and scaling
        return (value + 1) * 0.5

    def get_value(self, pos: V2) -> float:
        """Returns Perlin noise value between 0 and 1 at a given position."""
        # Convert pos to numpy array to be consistent with other operations
        pos_np = np.array([pos.x, pos.y])
        return self._get_value_at_grid_point(pos_np)


def smoothstep(t):
    return t**3 * (t * (t * 6 - 15) + 10)


def generate_noise_map(perlin, width, height, scale):
    """Generate the Perlin noise values for the entire screen."""
    noise_map = np.zeros((height, width), dtype=np.float32)

    for x in range(width):
        for y in range(height):
            noise_map[y, x] = perlin.get_value(V2(x/scale.x, y/scale.y))

    return noise_map


def interpolate_color(start_color, end_color, noise):
    smooth_noise = smoothstep(noise)
    
    # Interpolate each color channel
    r = int(start_color[0] + (end_color[0] - start_color[0]) * smooth_noise)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * smooth_noise)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * smooth_noise)

    # Ensure color values are clamped between 0 and 255
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    return (r, g, b)


# Initialize pygame
pygame.init()

# Set up the window dimensions and scale
width, height = 800, 600
scale = V2(10, 10)  # The scale of the grid (controls the "zoom" of the noise)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Perlin Noise Visualization")

# Initialize PerlinNoise
perlin = PerlinNoise(width, height, scale)

# Define color start and end
start_color = (0, 255, 255)  # Teal
end_color = (255, 0, 0)  # Red

# Generate the Perlin noise map once
noise_map = generate_noise_map(perlin, width, height, scale)

# Create the Pygame surface to hold the pixel data
surf = pygame.Surface((width, height))

# Use the noise map to fill the pixel array
pixels = np.zeros((width, height, 3), dtype=np.uint8)  # Ensure 3 channels for RGB

# Interpolate the colors based on the Perlin noise map
for y in range(height):
    for x in range(width):
        noise_value = noise_map[y, x]
        color = interpolate_color(start_color, end_color, noise_value)
        pixels[x, y] = color

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Convert the pixel array to a Pygame surface and display it
    # print(len(pixels.T), surf.get_size())
    surfarray.blit_array(surf, pixels)
    screen.blit(surf, (0, 0))

    pygame.display.flip()  # Update the display

# Quit pygame
pygame.quit()
