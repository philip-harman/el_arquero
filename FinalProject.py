from math import sin as sin
from math import cos as cos
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# user input
vel = 0 # 0 to 100 m/s
ang = 0 # Angle must be 0 to 90 (doesn't work below 0 for some reason...)


# Calculates arrow trajectory
def trajectory(vel, angle, wind):
    #Initial conditions
    posx = []
    posy = []
    g = 9.8
    rad_angle = math.radians(angle)

    # Hang time + 3 sec
    hangtime =  ((2 * vel * sin(rad_angle)) / g) + 3

    # Time array
    time = []
    for i in range(int(hangtime * 10)):
        time.append(i/10)
    time.append(hangtime)

    # Horizontal / Vertical pos. vs. time
    for t in time:
        posx.append((vel*cos(rad_angle)*t) + (1/2)*(wind)*(t**2))
        posy.append((vel*sin(rad_angle)*t) - (1/2)*(g)*(t**2))

    return posx,posy

# Imports background, sets misc. parameters
def initialize_plot():
    background = plt.imread("background.png")
    plt.imshow(background, extent = [-20,121,-22,60])
    plt.xlim(-20,121)
    plt.ylim(-22,60)
    plt.axis('off')
    plt.rcParams["figure.figsize"] = (60,40)


#Plots level's Target location + Walls + Wind direction indicator
def plot_level(level):
    # Plot walls
    for w in level.walls:
        plt.plot( w[0] , w[1] , color = '#BD4002' , linewidth = 25)

    # Display wind
    if level.wind == 0:
        pass
    elif level.wind > 0:
        for i in range(0,level.wind + 1,4):
            plt.scatter((i*0.65) + 97.6, -19.2, 4000, marker = '>', color = 'y')
    elif level.wind < 0:
        for i in range(level.wind, 2,4):
            plt.scatter((i*0.65) + 93.8, -19.2, 4000, marker = '<', color = 'y')

    # Plot target
    plt.scatter(level.target_x,level.target_y, 70000, marker = 's', color = '#BD4002')
    plt.scatter(level.target_x,level.target_y, 40000, marker = 's', color = 'w')
    plt.scatter(level.target_x,level.target_y, 20000, marker = 's', color = '#BD4002')
    plt.scatter(level.target_x,level.target_y, 5000, marker = 's', color = 'w')

    plt.show()


def plot_trajectory(vel,angle,level):
    # This will need to be revised: iterate thru trajectory, checking against hit_target/hit_wall
    # once hit_target or hit_wall = true, STOP iteration and print resulting trajectory + hit/miss
    # if iteration runs all the way thru and does not hit target, print 'MISS'

    final_trajectory = [ [] , [] ]
    posx, posy = trajectory(vel, angle, level.wind)
    for i in range(1,len(posx)):
        while hit_target == False and hit_wall == False:
            final_trajectory[0].append(posx)
            final_trajectory[1].append(posy)
        # if hit_target OR hit_wall = True, end.
        # call hit_target for final_trajectory values LAST and 2nd TO LAST in final_trajectory
        # NOTE: if hit_wall get's triggered first, has to be a miss.
        # Otherwise it could be possible to aim straight at the wall at high volecity
        # on some levels and still 'hit' the target due to the iteration rate of trajectory


        #if hit_target(x,y,level) == True:

    # Append x/y values to 'plotted trajectory' list to only show trajectory until
    #           arrow strikes something
    # Plot this staggered vs. time
    #plt.plot( x , y , color = 'red',linestyle = ':', linewidth = 10)


# To check for each segment of arrow trajectory and see if it intersects with any walls/target
def intersect(a1x, a2x, a1y, a2y, w1x, w2x, w1y, w2y):
    lines_intersect = False
    # ax/ay = Arrow head + tip coords
    # wx/wy = the above for each wall segment (or side of the target)

    # coefficient arrays y=mx+b (m = array[0], b = array[1])
    a_coefs = np.polyfit([a1x,a2x], [a1y, a2y], 1)
    w_coefs = np.polyfit([w1x,w2x], [w1y, w2y], 1)

    # Pass if slopes are equal (otherwise will error due to no intersection)
    # otherwise find x-point where lines intersect
    if a_coefs[0] == w_coefs[0]:
        pass
    else:
        x_int = (a_coefs[1] - w_coefs[1]) / (w_coefs[0] - a_coefs[0])

    # find if intersection occurs on line segment. If so, intersect = TRUE
    if a1x > a2x: # Intersection check for left to right trajectory
        if x_int < a1x and x_int > a2x: lines_intersect = True
    elif a2x >= a1x:
        if x_int < a2x and x_int > a1x: lines_intersect = True

    return lines_intersect

def hit_target(final_trajectory,level):
    hit_target = False
    # call intersect for last segment of final_trajectory + all four outer segmens of the target
    # NOTE: most recent pt of trajectory = a1. 2nd most recent = a2

    # target information found in level
    return hit_target


def hit_wall(final_trajectory, level):
    hit_wall = False
    # call intersect for last segment of final_trajectory + all wall segments
    # NOTE: most recent pt of trajectory = a1. 2nd most recent = a2

    # wall information found in level
    return hit_wall


#def invalid input
#(ALT IDEA - maybe pygame has some kind of slider that can be used?)


# Levels: Defines target location, wind, number and location of walls
class Level():
    def __init__(self, level, target_x, target_y, wind, walls):
        self.level = level
        self.target_x = target_x
        self.target_y = target_y
        self.wind = wind
        self.walls = walls

# Set up walls [[x1, x2],[y1, y2]] for each wall
walls_L1 = [ ]
walls_L2 = [[[20,20],[-15,20]]]
walls_L3 = [ [[52,68],[22,22]] , [[52,52],[22,38]] , [[68,68],[-15,38]] ]
walls_L4 = [ [[-20,25],[20,20]] , [[25,55],[35,35]] , [[55,85],[50,50]] , [[25,25],[20,35]] , [[55,55],[35,50]] , [[85,85],[50,56]] ]
walls_L5 = [ [[52,52],[-15,16]] , [[96,96],[16,30]] , [[108,108],[-15,30]] , [[52,96],[16,16]] , [[52,80],[16,40]] , [[80,96],[40,24]] ]

# Level information (Level # , target x, target y, wind, wall list)
L1 = Level(1, 80, 25, 0, walls_L1) # V = 36, A = 40
L2 = Level(2, 90, 0, 7, walls_L2)  # V = 23, A = 80
L3 = Level(3, 60, 30, 0, walls_L3) # V = 40, A = 78
L4 = Level(4, 0, 27, -20, walls_L4) # V = 91, A = 28
L5 = Level(5, 91, 0, -7, walls_L5) # V = 56, A = 45

lvl = L2

initialize_plot()
#plot_trajectory(92, 28, lvl)
plot_level(lvl)

print(intersect(0,4,0,4,-2,9,9,-2))
