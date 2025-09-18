
# say we want to get a noise value between a grid(grid) at some specific point(x)
# and we have a value x
x = 0.5
# with grid
grid = [0,1]

# say gradients are 
grads = [-1,1]

# displacements
disp = [x-grid[0], grid[1]-x]

# dot products
dot = [disp[0]*grads[0], disp[1]*grads[1]]

# interpolation, we have two methods:
#   1) linear { Interpolated Value= dot_product[0] × (1−t) + dot_product[1] × t }  where t is (x - lower) / (higher - lower)
#   2) linear_fade   { same as above but after calculating t, put it in [f(t) = t**3 * (t(6t - 15) + 10)] or any other fade_func that gives 0 for 0, 1 for 1 and gives a smooth curve for everything else}

# basically fade is an extention to linear interpolation and is pretty much option
# but it does produce a more smooth result so like, might as well use it

# linear interpolation
t = (x - grid[0]) / (grid[1] - grid[0])
val = dot[0] * (1-t) + dot[1] * t
print(val)

# linear_face interpolation
fade = lambda t: t**3 * (t*(t*6 - 15) + 10)

t = (x - grid[0]) / (grid[1] - grid[0])
t = fade(t)                     # only new thing
val = dot[0] * (1-t) + dot[1] * t
print(val)


# val is the final value that we return
