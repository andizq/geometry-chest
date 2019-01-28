import numpy as np
from matplotlib.patches import FancyArrow
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from argparse import ArgumentParser
import os

#**************************
#USER's INPUTs
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

#******************
#INITIAL CONDITIONS
#******************
vx = 20.
phi0 = 0
r0 = np.array([0, Rd])
t = np.linspace(0, 6 * 2*np.pi*Rp/abs(vx), 300) #6 Periods

#**********
#KINEMATICS
#**********
def circ_mv(vx,Rd,Rp,phi0,r0,t):
    phi = - vx * t / Rd + phi0 
    v = vx * np.array([1 + Rp/Rd * np.sin(phi), - Rp/Rd * np.cos(phi)])
    r = np.array([vx * t + Rp * np.cos(phi) + r0[0], Rp * np.sin(phi) + r0[1]]) 
    return r,v

rp,vp = circ_mv(vx,Rd,Rp,phi0,r0,t)
rd,vd = circ_mv(vx,Rd,Rd,phi0,r0,t)

#********************
#INITIALIZING OBJECTS
#********************
fig = plt.figure()
ylim_val = np.max([Rp,Rd])
ax = fig.add_subplot(111, xlim=(-10,100), ylim=(-2*ylim_val,4*ylim_val), aspect = 'equal')
ax.grid()
circle = plt.Circle((0, Rd), Rd, lw = 2, edgecolor='g', facecolor = 'none')
virt_circle = plt.Circle((0, Rp), Rp, lw = 1, ls = '-', edgecolor='cyan', facecolor = 'none')
floor = ax.axhline(-0.3, color = 'orange')
line, = ax.plot([], [], '-', color = 'blue', lw = 1.6, animated = True)
radius_seg, = ax.plot([], [], ':', color = 'black', lw = 1.4, animated = True)
dot_d, = ax.plot([], [], marker = 'o', color = 'gray', ms = 5)
dot_p, = ax.plot([], [], marker = 'o', color = 'red', ms = 6)

props = dict(boxstyle='round', facecolor='azure', alpha=0.5)
vel_text = ax.text(0.05, 1.3, '', transform=ax.transAxes, fontsize=6,
                   verticalalignment='top', bbox=props)

vector = FancyArrow(0, 0, 0, 0); vec_width = 0.15
vector_x = FancyArrow(0, 0, 0, 0); vecx_width = 0.12
vector_y = FancyArrow(0, 0, 0, 0); vecy_width = 0.12

objects = [circle, virt_circle, floor, line, radius_seg]
#*******************
#ANIMATION FUNCTIONS
#*******************
def init():
    line.set_data([],[])
    dot_p.set_data([],[])
    dot_d.set_data([],[])
    radius_seg.set_data([],[])
    ax.add_patch(circle)
    ax.add_patch(virt_circle)
    ax.add_patch(vector)
    ax.add_patch(vector_x)
    ax.add_patch(vector_y)
    return line, dot_p, dot_d, radius_seg

xlist, ylist = [], []    
def animate(i):
    
    global vector, vector_x, vector_y, vec_width, vecx_width, vecy_width

    ax.patches.remove(vector)
    ax.patches.remove(vector_x)
    ax.patches.remove(vector_y)

    xp, yp = rp[0][i], rp[1][i]
    xd, yd = rd[0][i], rd[1][i]
    vvx, vvy = np.array([vp[0][i], vp[1][i]]) / 7.

    xlist.append(xp)
    ylist.append(yp)
    xmin, xmax = ax.get_xlim()
    
    fmin, fmax = 1,1 
    if xp >= xmax or xp <= xmin:
        if xp >= xmax: fmax = 2
        else: fmin = 2
        ax.set_xlim(fmin*xmin, fmax*xmax)
        ylim_val = np.max([Rp,Rd])
        ax.set_ylim(-2*ylim_val, 4*ylim_val)
        for obj in objects: obj.set_linewidth(0.5*obj.get_linewidth())
        dot_p.set_markersize(0.5*dot_p.get_markersize())
        dot_d.set_markersize(0.5*dot_d.get_markersize())
        vec_width *= 0.5
        vecx_width *= 0.5
        vecy_width *= 0.5        
        vel_text.set_position((0.05, vel_text.get_position()[1] * 1.2))
        ax.figure.canvas.draw()        
    
    line.set_data(xlist, ylist)
    dot_p.set_data([xp], [yp])
    dot_d.set_data([xd], [yd])
    circle.center = (vx*t[i],Rd)
    xc, yc = virt_circle.center = circle.center
    radius_seg.set_data([xc, xp], [yc, yp])
    
    vector = FancyArrow(xp,yp,vvx,vvy, color = 'magenta', width=vec_width, head_width=5*vec_width)
    vector_x = FancyArrow(xp,yp,vvx,0, color = 'black', ls='-', width=vecx_width, head_width=5*vecx_width)
    vector_y = FancyArrow(xp,yp,0,vvy, color = 'black', ls='-', width=vecy_width, head_width=5*vecy_width)
    ax.add_patch(vector)
    ax.add_patch(vector_x)
    ax.add_patch(vector_y)

    textstr = '\n'.join((
            r'$v_{px}=%.2f$' % (vp[0][i], ),
            r'$v_{py}=%.2f$' % (vp[1][i], ),
            r'$||\vec{v}_p||=%.2f$' % (np.linalg.norm([vp[0][i], vp[1][i]]), ),
            r'$\vec{v}_{disc}=%.2f$ $\mu_x$' % (vx, )))
    
    vel_text.set_text(textstr)
    
    return line, dot_p, circle, floor, vector

#*****************
#ANIMATION & VIDEO
#*****************
interval = 50 #Frames delay in miliseconds
ani = animation.FuncAnimation(fig, animate, np.arange(0,len(t)),  
                              blit=True*1, interval=20,
                              init_func=init, repeat=False)

fps = 1000. / interval #Frames per second (1000 ms / interval)
ani.save(output, fps=fps, dpi=200)
os.system('open %s'%output)
