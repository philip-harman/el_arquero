import numpy as np
import math
from math import sin as sin
from math import cos as cos
import pygame
import time

# Sets up window for game
pygame.init()
size = (1100,650)
display = pygame.display.set_mode(size)

# Clears out plot between shots + levels (keeps background)
def reset_plot():
    display = pygame.display.set_mode(size)
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, size)
    display.blit(background, [0, 0])
    pygame.display.flip()

# Converts all x/y coordinates + calculations from old Jupyter window size to new Pygame window size.
def conv_x(x):
    x_new = 7.8101418*x + 156.028
    return x_new
def conv_y(y):
    y_new = (-7.9268293)*y + 475.609
    return y_new

# Defines parameters of each level (target locaiton, wind, wall locations)
# Also contains method to plot the level over the background image
class Level():
    def __init__(self, level, target_x, target_y, wind, walls):
        self.level = level
        self.target_x = conv_x(target_x)
        self.target_y = conv_y(target_y)
        self.wind = wind
        self.walls = walls
    def plot_level(self):
        # Plots walls
        for w in self.walls:
            x1 = conv_x(w[0][0])
            x2 = conv_x(w[0][1])
            y1 = conv_y(w[1][0])
            y2 = conv_y(w[1][1])
            pygame.draw.line(display, (189, 64, 2), (x1,y1), (x2,y2),15)
        # Display wind
        if self.wind == 0:
            pass
        elif self.wind > 0:
            pygame.draw.line(display, (240, 218, 15), (906,626), (906+(self.wind)*6.4,626),20)
        else:
            pygame.draw.line(display, (240, 218, 15), (906+(self.wind*6.4),626), (906,626),20)
        # Plots target
        pygame.draw.line(display, (0,111,255), (self.target_x - 40,self.target_y), (self.target_x + 40,self.target_y), 80)
        pygame.draw.line(display, (255,255,255), (self.target_x - 28,self.target_y), (self.target_x + 28,self.target_y), 56)
        pygame.draw.line(display, (0,111,255), (self.target_x - 13,self.target_y), (self.target_x + 13,self.target_y), 26)
        pygame.display.flip()

# Wall specs for each level [[x1, x2],[y1, y2]]
walls_L1 = []
walls_L2 = [[[20,20],[-15,20]]]
walls_L3 = [ [[52,68],[22,22]] , [[52,52],[22,38]] , [[68,68],[-15,38]] ]
walls_L4 = [ [[-20,25],[20,20]] , [[25,55],[35,35]] , [[55,85],[50,50]] , [[25,25],[20,35]] , [[55,55],[35,50]] , [[85,85],[50,56]] ]
walls_L5 = [ [[52,52],[-15,16]] , [[96,96],[16,30]] , [[108,108],[-15,30]] , [[52,96],[16,16]] ]

# Creates Level object for levels 1-5 (possible solutions included)
L1 = Level(1, 80, 25, 0, walls_L1) # V = 36, A = 40
L2 = Level(2, 90, 0, 7, walls_L2)  # V = 23, A = 80
L3 = Level(3, 60, 30, 0, walls_L3) # V = 40, A = 78
L4 = Level(4, 0, 27, -20, walls_L4) # V = 91, A = 28
L5 = Level(5, 91, 0, -7, walls_L5) # V = 56, A = 45
all_levels = [L1, L2, L3, L4, L5]

# Calculates full_trajectory array[x,y] from vel/angle/wind (Ignores obstacles)
def full_trajectory(vel, angle, wind):
    posx = []
    posy = []
    g = 9.8
    rad_angle = math.radians(angle)
    hangtime =  ((2 * vel * sin(rad_angle)) / g) + 5
    time = []
    for i in range(int(hangtime * 500)):
        time.append(i/500)
    time.append(hangtime)
    for t in time:
        posx.append(conv_x((vel*cos(rad_angle)*t) + (1/2)*(wind)*(t**2)))
        posy.append(conv_y((vel*sin(rad_angle)*t) - (1/2)*(g)*(t**2)))
    return posx, posy

# Iterates thru full_trajectory. Checks each point for collision w/ target or wall
# Returns final_trajectory & score
# Final_trajectory = full_trajectory UP TO collision detected; else, full trajectory.
# Score: Indicates bullseye(3), inner ring (2), outer ring (1) or miss (0)
def final_trajectory(vel,angle,level):
    final_trajectory = [[],[]]
    posx, posy = full_trajectory(vel, angle, level.wind)
    hit_score = [0]
    score = 0
    for i in range(8,len(posx)):
        final_trajectory[0].append(posx[i-8])
        final_trajectory[1].append(posy[i-8])
        if hit_wall(posx[i], posy[i], level) == True:
            score = 0
            break
        elif hit_target(posx[i], posy[i], level) > 0: hit_score.append(hit_target(posx[i], posy[i], level))
        if hit_target(posx[i], posy[i], level) < max(hit_score):
            score = max(hit_score)
            break
    return score, final_trajectory

# Plots final trajectory
def plot_final_trajectory(final_trajectory):
    for i in range(1,len(final_trajectory[0]),4):
        pygame.draw.line(display,(193,39,39), (final_trajectory[0][i-1], final_trajectory[1][i-1]),((final_trajectory[0][i], final_trajectory[1][i])), 5)
        pygame.display.flip()


# Checks each point in trajectory, flags if point is in target 'hit box'
def hit_target(x,y,level):
    hit_target = 0
    if collide(x, y, level.target_x - 13, level.target_x + 13, level.target_y - 13, level.target_y + 13) == True:
        hit_target = 3
    elif collide(x, y, level.target_x - 28, level.target_x + 28, level.target_y - 28, level.target_y + 28) == True:
        hit_target = 2
    elif collide(x, y, level.target_x - 40, level.target_x + 40, level.target_y - 40, level.target_y + 40) == True:
        hit_target = 1
    return hit_target

# Checks each point in traj for each wall in lvl, flags if point is in wall 'hit box'
def hit_wall(x,y,level):
    hit_wall = False
    for wall in level.walls:
        if collide(x, y, conv_x(wall[0][0]) - 7.5 , conv_x(wall[0][1]) + 7.5 ,conv_y(wall[1][1]) + 7.5,conv_y(wall[1][0]) - 7.5) == True:
            hit_wall = True
    return hit_wall

# Used in hit_wall and hit_target; flags if current point is in 'hit box'
def collide(x, y, wall_left, wall_right, wall_bottom, wall_top):
    collide = False
    if (min(wall_left,wall_right) < x < max(wall_left,wall_right)) and (min(wall_bottom,wall_top) < y < max(wall_bottom,wall_top)):
        collide = True
    return collide

# For printing messages on pygame screen
def p_a(txt,level = ''):
    if level == '':
        pass
    else:
        reset_plot()
        level.plot_level()
    font = pygame.font.SysFont(None, 25)
    screen_text = font.render(txt, True, (240, 218, 15))
    display.blit(screen_text, [200, 610])
    pygame.display.update()


# Requests input for velocity/angle, continues requesting until valid input received
# Also allows entry = 'q', which quits the game.
def user_input(level):
    valid_vel = False
    valid_ang = False
    p_a('Select Velocity [0-100] or quit [q]',level)
    while valid_vel == False:
        vel = input()
        if vel == 'q':
            break
        elif vel.isnumeric() == False:
            p_a('Error! Input must be [0-100] or [q].',level)
        elif 0 <= int(vel) <= 100:
            valid_vel = True
        else:
            p_a('Error! Velocity must be [0-100].',level)
    p_a('Select Angle (0-90) or quit [q]',level)
    while valid_ang == False and vel != 'q':
        ang = input()
        if ang == 'q':
            break
        elif ang.isnumeric() == False:
            p_a('Error! Input must be [0-90] or [q].',level)
        elif 0 <= int(ang) <= 90:
            valid_ang = True
        else:
            p_a('Error! Angle must be [0-90].',level)
    if vel == 'q' or ang == 'q':
        reset_plot()
        level.plot_level()
        return 'q' , 'q'
    else:
        return int(vel), int(ang)

# Announcements for hit/miss
def hit_miss_announcement(score):
    if score == 0: annc = 'Miss! Press [A + enter] to try again.'
    elif score == 1: annc = 'Nice! Press [A + enter] to continue.'
    elif score == 2: annc = 'Great shot! Press [A + enter] to continue.'
    elif score == 3: annc = 'Bullseye! Press [A + enter] to continue.'
    return annc

# Manages game logic flow
def run_game(all_levels):
    reset_plot()
    time.sleep(2)
    p_a('Welcome to EL ARQUERO')
    time.sleep(2)
    vel = 0
    ang = 0
    for L in range(len(all_levels)):
        score = 0
        p_a('LEVEL '+str(all_levels[L].level),all_levels[L])
        time.sleep(2)
        while score == 0 and (vel != 'q' and ang != 'q'):
            all_levels[L].plot_level()
            vel, ang = user_input(all_levels[L])
            if vel == 'q': break
            score, final_traj = final_trajectory(vel, ang, all_levels[L])
            plot_final_trajectory(final_traj)
            pygame.display.flip()
            p_a(hit_miss_announcement(score),all_levels[L])
            cont = input()
        if vel == 'q' or ang == 'q': break
        else: time.sleep(1)
    if vel == 'q' or ang == 'q': p_a('User quit :(',all_levels[0])
    else: p_a('You win!',all_levels[4])
    time.sleep(1)
    pygame.quit()
    quit

run_game(all_levels)
