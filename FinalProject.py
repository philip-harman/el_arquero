import matplotlib.pyplot as plt
import numpy as np
import math
from math import sin as sin
from math import cos as cos

# user input
vel = 0 # 0 to 100 m/s
ang = 0 # Angle must be 0 to 90 (doesn't work below 0 for some reason...)


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


def initialize_plot():
    background = plt.imread("background.png")
    plt.imshow(background, extent = [-20,121,-22,60])
    plt.xlim(-20,121)
    plt.ylim(-22,60)
    plt.axis('off')
    plt.rcParams["figure.figsize"] = (60,40)


#Plots level's Target location + Walls + Wind direction
def plot_level(level):
    # Plot target
    target = plt.imread("target.jpg")
    plt.imshow(target, extent = [level.target_x-5,level.target_x+5,level.target_y-5,level.target_y+5])

    # Plot walls
    for w in level.walls:
        plt.plot( w[0] , w[1] , color = '#BD4002' , linewidth = 25)

    # Display wind
    wind = plt.imread("wind.jpg")
    plt.imshow(wind, extent = [96.3 + level.wind*1.53, 96.3, -20, -18.4])
    plt.show()


def plot_trajectory(vel,angle,wind):
    # This will need to be revised: iterate thru trajectory, checking against hit_target/hit_wall
    # once hit_target or hit_wall = true, STOP iteration and print resulting trajectory + hit/miss
    # if iteration runs all the way thru and does not hit target, print 'MISS'
    x,y = trajectory(vel,angle,wind)
    plt.plot( x , y , color = 'red',linestyle = ':', linewidth = 10)


#def hit_target
#def hit_wall: will need to defined a range 0f +/- X for vert and +/- Y for horiz walls
        # because it's unlikely an exact iterated point of trajectory will collide with the wall

#def invalid input (ALT IDEA - maybe pygame has some kind of slider that can be used?)


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
walls_L5 = [ [[52,52],[-15,16]] , [[96,96],[16,30]] , [[108,108],[-15,30]] , [[52,96],[16,16]] , [[52,80],[16,40]] , [[80,96],[40,24]] ]


# In work
walls_L4 = [ [[1,1],[1,3]] , [[2,2],[0,2]] , [[0,2.5],[0,0]] , [[3,3],[0,3]] ]



# Level information (Level # , target x, target y, wind, wall list)
# NOTE: Wind can be anywhere from -10 to 10
L1 = Level(1, 80, 25, 0, walls_L1) # V = 36, A = 40
L2 = Level(2, 90, 0, 7, walls_L2)  # V = 23, A = 80
L3 = Level(4, 60, 30, 0, walls_L3) # V = 40, A = 78
L5 = Level(3, 91, 0, -7, walls_L5) # V = 56, A = 45

# In work
L4 = Level(5, -10, 27, 0, walls_L4) # curve back up and left, strong wind to left



lvl = L4

initialize_plot()
plot_trajectory(56,45,lvl.wind)
plot_level(lvl)
