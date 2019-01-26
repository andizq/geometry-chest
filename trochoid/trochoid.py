import numpy as np
from matplotlib.patches import FancyArrow
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from argparse import ArgumentParser
import os

#**************************
#USER's INPUT
#**************************
parser = ArgumentParser(prog='Trochoids', description='Drawing trochoids!')
parser.add_argument('-Rd', '--Rd', help='Radius of the reference disc. Defaults to 5')
parser.add_argument('-Rp', '--Rp', help='Radius of the circle that will trace the trochoid. Defaults to 2*Rd')
parser.add_argument('-o', '--output', help="Name of the resulting mp4 video. Defaults to 'mv_trochoid.mp4'")
args = parser.parse_args()

if args.Rd is not None: Rd = float(args.Rd)
else: Rd = 5.

if args.Rp is not None: Rp = float(args.Rp)
else: Rp = 2*Rd

if args.output is not None: output = args.output
else: output = 'mv_trochoid.mp4'

#----------
#KINEMATICS
#----------
def circ_mv(vx,Rd,Rp,phi0,r0,t):
    phi = - vx * t / Rd + phi0 
    v = vx * np.array([1 + Rp/Rd * np.sin(phi), - Rp/Rd * np.cos(phi)])
    r = np.array([vx * t + Rp * np.cos(phi) + r0[0], Rp * np.sin(phi) + r0[1]]) 
    return r,v

vx = 20.
phi0 = -np.pi/2 * 0
r0 = np.array([0, Rd])
t = np.linspace(0, 6 * 2*np.pi*Rp/abs(vx), 300) #6 Periods

r1,v1 = circ_mv(vx,Rd,Rp,phi0,r0,t)

#-------------
#-------------

#--------
#PLOTTING
#--------

fig = plt.figure()
ax = fig.add_subplot(111, xlim=(-10,100), ylim=(-2*Rd,4*Rd), aspect = 'equal')
circle = plt.Circle((0, Rd), Rd, lw = 2, edgecolor='g', facecolor = 'none')
virt_circle = plt.Circle((0, Rp), Rp, lw = 1, ls = '-', edgecolor='cyan', facecolor = 'none')
floor = ax.axhline(-0.3, color = 'orange')

line, = ax.plot([], [], '-', color = 'blue', lw = 1.6, animated = True) #marker = 'o')
dot, = ax.plot([], [], marker = 'o', color = 'red', ms = 6)
radius, = ax.plot([], [], ':', color = 'black', lw = 1.4, animated = True) #marker = 'o')
vector = FancyArrow(0, 0, 0, 0); vec_width = 0.15
vector_x = FancyArrow(0, 0, 0, 0); vecx_width = 0.12
vector_y = FancyArrow(0, 0, 0, 0); vecy_width = 0.12
 
ax.grid()
xlist, ylist = [], []

def init():
    #ax.set_xlim(-10, 100)
    #ax.set_ylim(-2*Rp, 4*Rp)
    line.set_data([],[])
    dot.set_data([],[])
    radius.set_data([],[])
    ax.add_patch(circle)
    ax.add_patch(virt_circle)
    ax.add_patch(vector)
    ax.add_patch(vector_x)
    ax.add_patch(vector_y)
    return line, dot, radius
    
def animate(i):
    
    global vector, vector_x, vector_y, vec_width, vecx_width, vecy_width

    ax.patches.remove(vector)
    ax.patches.remove(vector_x)
    ax.patches.remove(vector_y)

    x, y = r1[0][i], r1[1][i]
    vvx, vvy = np.array([v1[0][i], v1[1][i]]) / 7.

    xlist.append(x)
    ylist.append(y)
    xmin, xmax = ax.get_xlim()
    
    fmin, fmax = 1,1
    if x >= xmax or x <= xmin:
        if x >= xmax: fmax = 2
        else: fmin = 2
        ax.set_xlim(fmin*xmin, fmax*xmax)
        ax.set_ylim(-2*Rd, 4*Rd)
        circle.set_linewidth(0.5*circle.get_linewidth())
        virt_circle.set_linewidth(0.5*virt_circle.get_linewidth())
        floor.set_linewidth(0.5*floor.get_linewidth())
        radius.set_linewidth(0.5*radius.get_linewidth())
        line.set_linewidth(0.5*line.get_linewidth())
        dot.set_markersize(0.5*dot.get_markersize())
        vec_width *= 0.5
        vecx_width *= 0.5
        vecy_width *= 0.5
        
        ax.figure.canvas.draw()        
    
    line.set_data(xlist, ylist)
    dot.set_data([x], [y])
    circle.center = (vx*t[i],Rd)
    virt_circle.center = circle.center
    xc, yc = circle.center
    radius.set_data([xc, x], [yc, y])
    
    vector = FancyArrow(x,y,vvx,vvy, color = 'magenta', width=vec_width, head_width=5*vec_width)
    vector_x = FancyArrow(x,y,vvx,0, color = 'black', ls='-', width=vecx_width, head_width=5*vecx_width)
    vector_y = FancyArrow(x,y,0,vvy, color = 'black', ls='-', width=vecy_width, head_width=5*vecy_width)
    ax.add_patch(vector)
    ax.add_patch(vector_x)
    ax.add_patch(vector_y)

    return line, dot, circle, floor, vector


#-----------------
#ANIMATION & VIDEO
#-----------------
interval = 50 #Delay between frames in miliseconds
ani = animation.FuncAnimation(fig, animate, np.arange(0,len(t)),  
                              blit=True*1, interval=20,
                              init_func=init, repeat=False)

fps = 1000. / interval #Frames per second (1000 ms / interval)
name_video = output
ani.save(name_video, fps=fps, dpi=200)
os.system('open %s'%name_video)
