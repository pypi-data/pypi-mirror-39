import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

''''
Creates a fractal image

Returns a fractal image

Parameters:
f = autodiff function
area = ((x_min, x_max), (y_min, y_max))
size = (x_size, y_size)
diff_method="AD" or "Finite"
e = Epsilon of iterations
max_iters = Maximum number of iterations
alpha = Iterative tuning parameter
'''
def create_fractal(f, size, area, diff_method="AD", e=1e-3, max_iters=50, alpha=1,):
    grid_root, grid_iter, roots = fractal_grid(f, size, area, "Finite", e, max_iters, alpha)
    image = grid_to_image(grid_root,grid_iter,roots)
    return image


# Returns (root, iterations) if converges
def newtons_method(f, z, diff_method = "AD", e=1e-3, max_iters=50, alpha=1):
    f(x=z)
    for i in range(max_iters):
        if diff_method == "Finite":
            derivative = finite_difference(f,z)
        else:
            derivative =f.derivative()["x"]
        zplus = z - alpha*f.value()/derivative
        # Checks for convergence
        if abs(zplus - z) < e:
            return (z, i)
        z = zplus
    return None


def finite_difference(f, z, epsilon=1e-3):
    return (f(x=(z+epsilon)).value() - f(x=z).value()) / epsilon

''''
Fractal grid

Returns (array_of_roots, array_of_iterations, roots_found)

Parameters:
f = autodiff function
area = ((x_min, x_max), (y_min, y_max))
size = (x_size, y_size)
e = Epsilon of iterations
max_iters = Maximum number of iterations
alpha = Iterative tuning parameter
'''
def fractal_grid(f, size, area, diff_method="AD", e=1e-3, max_iters=50, alpha=1, ):
    # Parameters
    roots = []
    ((x_min, x_max), (y_min, y_max)) = area
    (x_size, y_size) = size

    # Outputs
    grid_root = np.zeros((y_size, x_size))
    grid_iter = np.zeros((y_size, x_size))

    # Grid calculations over complex plane
    for y in (range(y_size)):
        z_y = y * (y_max - y_min)/(y_size - 1) + y_min
        for x in range(x_size):
            z_x = x * (x_max - x_min)/(x_size - 1) + x_min
            found = newtons_method(f, complex(z_x, z_y), diff_method, e, max_iters)
            if found:
                root, iters = found

                flag = False
                for test_root in roots:
                    if abs(test_root - root) < e:
                        root = test_root
                        flag = True
                        break
                if not flag:
                    roots.append(root)

                grid_root[y,x] = roots.index(root)+1
                grid_iter[y,x] = iters

    return (grid_root, grid_iter, roots)

'''
Helper function to map a grid to a scaled output [0,255]
'''
def grid_to_image(grid_root, grid_iter, roots):
    img = np.zeros((grid_root.shape))
    idxs = np.linspace(0,255,len(roots),dtype=int)

#     grid_iter = np.log(grid_iter)
    scaled = grid_iter/np.max(grid_iter)

    shift = scaled*(256/4)

    for i in range(len(roots)):
        img[grid_root==i+1] = idxs[i]+shift[grid_root==i+1]
#         img[grid_root==i+1] = idxs[i]

    return img

'''
Function that saves frame into a video file
'''
def save_video(frames, filename, display=True):
    fig = plt.figure()
    ims = []
    for i in range(len(frames)):
        im = plt.imshow(frames[i], animated=True)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)
    if display:
        plt.show()
    ani.save(filename)