import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Model Parameters
a = 5 # semi-major axis
b = 3 # semi-minor axis
c = 4 # focal distance such that a^2 = b^2 + c^2
T = 3 # period
alphaTolerance = 0.0001; # radians
P = 4*T # period of precession
H = 2*math.pi*a*b/P # when doing precession
#H = 0 # set to zero when not doing precession

# Animation Parameters
totalTime = P # total time of animation in seconds
timeStep = 1/50; # time step in seconds

##########################################################

# Find swept area from alpha parameter.
def A(alpha):
    return ( a*alpha + c*math.sin(alpha) ) * b / 2

# Inverse of area function.
# Find alpha parameter from swept area.
def A_inverse(S):
    temp = S/(math.pi*a*b);
    p = 2*math.pi * math.floor(temp)
    q = 2*math.pi * math.ceil(temp)
    while(True):
        alpha = (p + q) / 2
        if q - p < alphaTolerance:
            return alpha
        if A(alpha) > S:
            q = alpha
        else: 
            p = alpha
    
# Find alpha parameter as a function of time. 
def f(t):
    return A_inverse(math.pi*a*b*t/T)

# Find x coordinate of the path as function of time.
def x(t):
    return a*math.cos(f(t)) + c

# Find y coordinate of the path as function of time.
def y(t):
    return b*math.sin(f(t))

###########################################################

# Subroutine for arctanktan_modified().
def atktsub(x, k):
    return math.atan2(k * math.sin(x), math.cos(x))

# Modified version of the function x -> arctan(k*tan(x))
# The modified version agrees with arctan(k*tan(x)) on (-pi/2, pi/2).
# It is defined for all real x, and has derivative k/( cos^2(x) + k^2*sin^2(x) ).
def arctanktan_modified(x, k):
    pi = math.pi
    n = round(x / pi)
    npi = n*pi
    if k > 0:
        return atktsub(x - npi, k) + npi
    elif k < 0:
        return atktsub(x - npi, k) - npi
    else:
        return 0
    
############################################################
    
# Find the precession angle as a function of time.
def g(t):
    k = math.sqrt((a-c)/(a+c))
    return H * (T/(math.pi*a*b))*arctanktan_modified(f(t)/2, k)

# Find X coordinate of the path as function of time when doing precession.
def X(t):
    temp = g(t)
    return math.cos(temp)*x(t) - math.sin(temp)*y(t)

# Find Y coordinate of the path as function of time when doing precession.
def Y(t):
    temp = g(t)
    return math.sin(temp)*x(t) + math.cos(temp)*y(t)

###########################################################
# ANIMATION USING X(t) and Y(t)

# Find the frame count.
frameCount = int(totalTime/timeStep);

# MAIN CALCULATION
tArray = np.linspace(0, totalTime, frameCount);
xArray = np.array([X(t) for t in tArray]);
yArray = np.array([Y(t) for t in tArray]);

# Create the figure.
fig, ax = plt.subplots()
ax.set_aspect('equal')
border = 0.2
ax.set_xlim(-c-a - border, c+a + border)
ax.set_ylim(-c-a - border , c+a + border)

# Declare the objects to animate.
line, = ax.plot([], [], 'k-', lw=2) # k- is black solid
dot, = ax.plot([], [], 'bo', markersize=6) # bo is blue dot
sun_dot, = ax.plot([0], [0], 'yo', markersize=12)  # yo is yellow dot

# Animatation functions.
def init():
    line.set_data([], [])
    dot.set_data([], [])
    return line, dot, sun_dot

def update(frame):
    line.set_data(xArray[:frame+1], yArray[:frame+1])
    dot.set_data(xArray[frame], yArray[frame])
    return line, dot, sun_dot

# Run the animation.
timeStepInMilliseconds = timeStep * 1000;
ani = FuncAnimation(fig, update, frameCount, init_func=init, blit=True, interval=timeStepInMilliseconds)

###########################################################
# Save the animation if desired.
# ani.save("animation.gif", writer='pillow', fps=1000 // timeStepInMilliseconds)

plt.show()
