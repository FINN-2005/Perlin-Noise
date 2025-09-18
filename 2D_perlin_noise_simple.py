from random import uniform


class V2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other): return V2(other.x + self.x, other.y + self.y)
    def __sub__(self, other): return V2(self.x - other.x, self.y - other.y)
    def __repr__(self): return f'V2({self.x:.3f}, {self.y:.3f})'


# Function to generate random gradient vector between -1 and 1
def get_random_vec() -> V2:
    return V2(uniform(-1, 1), uniform(-1, 1))

# Fade function for Perlin noise
def fade(t):
    return t**3 * (t * (t * 6 - 15) + 10)

# Set the grid size
n = V2(5, 3)  # Grid size: 5x3

# Given point in space for which we want to calculate the Perlin noise value
given = V2(2.5, 2)

# Generate 2D grid with gradient vectors
grid = [[get_random_vec() for _ in range(int(n.y))] for _ in range(int(n.x))]

# Interpolation function for 2D Perlin noise
# Interpolation function for 2D Perlin noise
def perlin_noise(given: V2):
    # Find the surrounding grid points
    lower = V2(int(given.x), int(given.y))
    higher = lower + V2(1, 1)

    # Ensure the higher grid point is within the grid bounds
    if higher.x >= n.x: higher.x = lower.x
    if higher.y >= n.y: higher.y = lower.y

    # Displacement vectors from the point to the lower and higher grid points
    disp0 = given - lower
    disp1 = higher - given

    # Get gradients at the four corners of the grid cell
    top_left = grid[int(lower.x)][int(lower.y)]
    top_right = grid[int(lower.x)][int(higher.y)]
    bottom_left = grid[int(higher.x)][int(lower.y)]
    bottom_right = grid[int(higher.x)][int(higher.y)]

    # Dot products of the gradient and displacement vectors for each corner
    dot_top_left = top_left.x * disp0.x + top_left.y * disp0.y
    dot_top_right = top_right.x * disp0.x + top_right.y * disp1.y
    dot_bottom_left = bottom_left.x * disp1.x + bottom_left.y * disp0.y
    dot_bottom_right = bottom_right.x * disp1.x + bottom_right.y * disp1.y

    # Interpolate along x-axis
    t_x = fade(disp0.x)  # Apply fade to the x-displacement
    interp_x_0 = dot_top_left * (1 - t_x) + dot_bottom_left * t_x
    interp_x_1 = dot_top_right * (1 - t_x) + dot_bottom_right * t_x

    # Interpolate along y-axis
    t_y = fade(disp0.y)  # Apply fade to the y-displacement
    result = interp_x_0 * (1 - t_y) + interp_x_1 * t_y

    return (result+1)/2

# Testing the function by getting Perlin noise value at 'given' point
noise_value = perlin_noise(given)
print(f"Perlin noise value at {given}: {noise_value}")
