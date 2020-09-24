import matplotlib.pyplot as plt
import numpy as np
import math
from math import sin as sin
from math import cos as cos
import matplotlib.patches as patches

#def

#def invalid_input


def trajectory(vel, angle, wind):
    posx = []
    posy = []
    g = 9.8
    rad_angle = math.radians(angle)
    hangtime =  ((2 * vel * sin(rad_angle)) / g) + 3
    time = []
    for i in range(int(hangtime * 110)):
        time.append(i/110)
    time.append(hangtime)
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


def plot_trajectory(vel,angle,level):
    final_trajectory = [[],[]]
    posx, posy = trajectory(vel, angle, level.wind)
    hit_score = [0]
    score = 0
    for i in range(3,len(posx)):
        final_trajectory[0].append(posx[i-3])
        final_trajectory[1].append(posy[i-3])
        if hit_target(posx[i], posy[i], level) > 0: hit_score.append(hit_target(posx[i], posy[i], level))
        if hit_wall(posx[i], posy[i], level) == True:
            score = 0
            break
        elif hit_target(posx[i], posy[i], level) < max(hit_score):
            score = max(hit_score)
            break

    # Plot this staggered vs. time in final version
    plt.plot(final_trajectory[0], final_trajectory[1] , color = 'red', linestyle = '-', linewidth = 10)

    if score == 0:
        print('Miss!')
        # have user try again
    else:
        if score == 1: print('Good shot!')
        if score == 2: print('Awesome!')
        if score == 3: print('Bullseye!')
        # next_level function


def hit_target(x,y,level):
    hit_target = 0
    if collide(x, y, level.target_x - 1.8, level.target_x + 1.8, level.target_y - 1.8, level.target_y + 1.8) == True:
        hit_target = 3
    elif collide(x, y, level.target_x - 3.5, level.target_x + 3.5, level.target_y - 3.5, level.target_y + 3.5) == True:
        hit_target = 2
    elif collide(x, y, level.target_x - 5.6, level.target_x + 5.6, level.target_y - 5.6, level.target_y + 5.6) == True:
        hit_target = 1
    return hit_target


def hit_wall(x,y,level):
    hit_wall = False
    for wall in level.walls:
        if collide(x, y, wall[0][0] - 1, wall[0][1] + 1, wall[1][0] - 1, wall[1][1] + 1) == True:
            hit_wall = True
    return hit_wall


def collide(x, y, wall_left, wall_right, wall_bottom, wall_top):
    collide = False
    if (wall_left < x < wall_right) and (wall_bottom < y < wall_top):
        collide = True
    return collide


class Level():
    def __init__(self, level, target_x, target_y, wind, walls):
        self.level = level
        self.target_x = target_x
        self.target_y = target_y
        self.wind = wind
        self.walls = walls
    def plot_level(self):
        # Plot walls
        for w in self.walls:
            plt.plot( w[0] , w[1] , color = '#BD4002' , linewidth = 25)
        # Display wind
        if self.wind == 0:
            pass
        elif self.wind > 0:
            for i in range(0,self.wind + 1,4):
                plt.scatter((i*0.65) + 97.6, -19.2, 4000, marker = '>', color = 'y')
        elif self.wind < 0:
            for i in range(self.wind, 2,4):
                plt.scatter((i*0.65) + 93.8, -19.2, 4000, marker = '<', color = 'y')
        # Plot target
        size = [70000, 35000, 10000]
        color = ['b', 'w', 'b']
        for i in range(3):
            plt.scatter(self.target_x,self.target_y, size[i], marker = 's', color = color[i])
        plt.show()

        # Set up walls [[x1, x2],[y1, y2]] for each wall
walls_L1 = []
walls_L2 = [[[20,20],[-15,20]]]
walls_L3 = [ [[52,68],[22,22]] , [[52,52],[22,38]] , [[68,68],[-15,38]] ]
walls_L4 = [ [[-20,25],[20,20]] , [[25,55],[35,35]] , [[55,85],[50,50]] , [[25,25],[20,35]] , [[55,55],[35,50]] , [[85,85],[50,56]] ]
walls_L5 = [ [[52,52],[-15,16]] , [[96,96],[16,30]] , [[108,108],[-15,30]] , [[52,96],[16,16]] ]

# Level information (Level # , target x, target y, wind, wall list)
L1 = Level(1, 80, 25, 0, walls_L1) # V = 36, A = 40
L2 = Level(2, 90, 0, 7, walls_L2)  # V = 23, A = 80
L3 = Level(3, 60, 30, 0, walls_L3) # V = 40, A = 78
L4 = Level(4, 0, 27, -20, walls_L4) # V = 91, A = 28
L5 = Level(5, 91, 0, -7, walls_L5) # V = 56, A = 45

lvl = L3

initialize_plot()
plot_trajectory(39, 78, lvl)
lvl.plot_level()
