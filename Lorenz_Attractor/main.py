import matplotlib.pyplot as plt

# Given the equations, defining the values of parameters
sigma = 10
beta = 8/3
rho= 28
dt = 0.01

# Get Equations
def equations(a, b, c):
    return sigma*(b-a), rho*a-a*c-b, a*b-beta*c


def f_coordinates(x, y, z):
    n = 13500 #steps
    t = 2
    
    #Initialize empty arrays for coordinates of X, Y, Z
    x_new = []
    y_new = []
    z_new = []
    
    #Determine coordinates of the point, step-by-step
    for i in range(n):
        dxdt, dydt, dzdt = equations(x, y, z)
        dx = dxdt * dt
        dy = dydt * dt
        dz = dzdt * dt
        
        x = x + dx
        y = y + dy
        z = z + dz
        t = t + dt
        
        x_new.append(x)
        y_new.append(y)
        z_new.append(z)
        

    # Plot
    r = plt.figure().add_subplot(projection='3d')
    r.plot(x_new, y_new, z_new, lw=0.5)
    r.set_xlabel("x")
    r.set_ylabel("y")
    r.set_zlabel("z")
    r.set_title("Lorenz Attractor", fontname="Times New Roman", fontweight="bold", fontsize=18)
    plt.savefig('xyz.png')
    plt.show()


    fig, u = plt.subplots(1, 3, sharex=False, sharey=False, figsize=(17, 6))
    
    # plot the x values vs the y values
    u[0].plot(x_new, y_new, color='r', alpha=0.7, linewidth=0.3)
    u[0].set_title('X-Y phase plane', fontweight="bold" )
    # plot the x values vs the z values
    u[1].plot(x_new, z_new, color='m', alpha=0.7, linewidth=0.3)
    u[1].set_title('X-Z phase plane', fontweight="bold")
    # plot the y values vs the z values
    u[2].plot(y_new, z_new, color='b', alpha=0.7, linewidth=0.3)
    u[2].set_title('Y-Z phase plane', fontweight="bold")

    plt.savefig("subplots.png")
    plt.show()

if __name__ == '__main__':    
    f_coordinates(0., 1., 1.05)
