### Importing all the necessary packages ###

import numpy as np
from math import *

"This file is defining all the important variables regarding drones characteristics. It allows as well to generate "
"the swarm configuration desired at the beginning of the simulation. During the simulation, several functions of this file are called  "
"in order to update some drone's parameters such as its position, its damage capability etc. The function get_drone_destroyed is also called "
"from this file to destroy a drone once it has been allocated. "


### Defining a drone class so each drone of the swarm is represented by a Python object. ###
class Drone:
    def __init__(self, pos, idx, close_drone=None):
        self.active = 1                                                         # says if the drone is still in operating state
        self.close_drone = close_drone
        self.pos = pos                                                          # Position of the drone
        self.idx = idx                                                          # Each drone is identified by an index
        self.threat_val = 1                                                     # Threat value of the drone

        self.speed = 1.0                                                        # Drone's velocity
        self.drone_escaped = False                                              # Drone's status represented as a Boolean to know
                                                                                # if the drone escaped the GBAD system range.
        self.drone_dist = 0.60                                                  # Variable representing the distance
                                                                                # to calculate the function value.
        self.damage = 0.50                                                      # Variable representing the damage capability
                                                                                # to calculate the function value.
        self.target_survivability = 1-0.635                                     # Variable representing the drone's survivability
                                                                                # to calculate the function value.
        self.engagement_zone = 0.60




### Function to destroy a drone or not depending on the probability of kill of the weapon used. ###
    def drone_get_destroyed(self, drone, weapon, base, simu):
        if weapon.ammunition > 0:
            if np.random.rand() < weapon.Pc:                                    # if the drone has been hit.
                if drone.active == 1:                                           # checking if it has not been already destroyed before.
                    simu.counter_drones_destroyed += 1                          # counting the number of drones destroyed in the simulator
                    simu.score += drone.threat_val                              # updating the score of the simulation
                drone.active = 0                                                # set the active status to zero if the drone is destroyed.
                return True
            else:                                                               # else the drone has been missed
                drone.target_survivability += 0.045                             # increasing its survivability in that case
                simu.surv_weapons[weapon.name][drone.idx] += 0.08*weapon.Pc
                return False
        weapon.ammunition += -1                                                 # whatever the drone is hit or drone, ammunition has been consumed



### Function to know whether a drone has escaped the range of a particular weapon ###
    def drone_escape(self, weapon, base):
        answer = False                                                          # assuming initially that the drone is in the range of the weapon
        if self.drone_escaped == False:                                         # checking if the drone hasn't already escaped weapon's range
            if np.linalg.norm(self.pos - np.array([0, 0, 0])) < weapon.range_window[0]:
                answer = True
                self.drone_escaped = True
                base.health -= 0.01 * self.damage                               # in the case where the drone escaped the weapon's range, we reduce the GBAD_health as

        return answer


### Function to update the drone's position at each time step of the simulation ###
    def update_drone_pos(self, time):
        direction_vec = - self.pos
        velocity_vec = direction_vec / np.linalg.norm(direction_vec)
        velocity_vec = np.array(velocity_vec * self.speed)
        self.pos = np.array(self.pos, dtype= np.float64)
        self.pos += velocity_vec * time
        self.drone_dist += 0.01

### Function to update the threat value of a drone ###
    def update_TV(self):
        pos_base = np.array([0, 0, 0])
        distance_of_drone = np.linalg.norm(self.pos - pos_base)
        threat_val = 1/distance_of_drone                                        # Initially, we were setting the threat value as 1/distance_of_drone.
        self.threat_val = threat_val
        return self.threat_val


### The next three functions are used to make the weights used by the value function dynamic ###
    def get_lambda(self, weapon, base):
        GBAD_health = base.health
        if GBAD_health == 0:
            return 5
        else :
            return 5*np.exp(-1/(1/GBAD_health)-1)

    def get_alpha(self, weight_init, time) :
        return weight_init*np.exp(1/(60*self.damage + time +0.1))


    def get_beta(self, base):
        GBAD_health = base.health
        if GBAD_health == 1:
            return 1
        else:
            return 10*np.exp(1/(GBAD_health - 1))




### The following class and methods are used to get all the initial position of the swarm in the desired formation ###

### Wave formation class ###
class Wave:
    def __init__(self,number_drones, head_position, angle, spacing):
        self.head_position = head_position                                     # Define the central position of the wave formation.
        self.angle = angle                                                     # Define the angle between the two branches of the wave.
        self.spacing = spacing                                                 # Define the space between each drone.
        self.number_drones = number_drones                                     # Define the number of drones in the swarm
        self.drone_list = []
        self.get_init_pos_wave()

### Function to get the initial positions of each drone in the swarm in a wave formation ###
    def get_init_pos_wave(self):
        nbr = (self.number_drones - 1) // 2
        nbl = (self.number_drones - 1) - nbr
        x_dist, y_dist = self.spacing * abs(np.sin(self.angle / 2)), self.spacing * abs(np.cos(self.angle / 2))
        left_side, right_side = np.zeros((nbl, 3)), np.zeros((nbr, 3))
        for l in range(0, nbl):
            left_side[l][0], left_side[l][1], left_side[l][2] = self.head_position[0] - (l + 1) * x_dist, self.head_position[1] - (
                    l + 1) * y_dist, self.head_position[2]
            point1 = left_side[l]
            drl = Drone(point1, l, 0)
            self.drone_list.append(drl)
        self.drone_list.append(Drone(self.head_position ,nbl, 0))
        for r in range(0, nbr):
            right_side[r][0], right_side[r][1], right_side[r][2] = self.head_position[0] + (r + 1) * x_dist, self.head_position[1] - (
                        r + 1) * y_dist, self.head_position[2]
            point2 = right_side[r]
            drr = Drone(point2, r+nbl, 0)
            self.drone_list.append(drr)
        pos = np.vstack((np.vstack((np.array(self.head_position), left_side)), right_side))



        # To get a double wave formation #

### Function to get the initial positions of each drone in the swarm in a double wave formation ###
    def get_init_double_wave(self):

        nbr = (self.number_drones - 1) // 2
        nbl = (self.number_drones - 1) - nbr
        x_dist, y_dist = self.spacing * abs(np.sin(self.angle / 2)), self.spacing * abs(np.cos(self.angle / 2))
        left_side1, right_side1 = np.zeros((nbl, 3)), np.zeros((nbr, 3))
        ###############################1ST WAVE#############################3###
        for l in range(0, nbl):
            left_side1[l][0], left_side1[l][1], left_side1[l][2] = self.head_position[0] - (l + 1) * x_dist, \
                                                                self.head_position[1] - (
                                                                        l + 1) * y_dist, self.head_position[2]
            point1 = left_side1[l]
            drl = Drone(point1, l, 0)
            self.drone_list.append(drl)
        self.drone_list.append(self.head_position)
        for r in range(0, nbr):
            right_side1[r][0], right_side1[r][1], right_side1[r][2] = self.head_position[0] + (r + 1) * x_dist, \
                                                                   self.head_position[1] - (
                                                                           r + 1) * y_dist, self.head_position[2]
            point2 = right_side1[r]
            drr = Drone(point2, r + nbl, 0)
            self.drone_list.append(drr)
        pos1 = np.vstack((np.vstack((np.array(self.head_position), left_side1)), right_side1))

        left_side2, right_side2 = np.zeros((nbl, 3)), np.zeros((nbr, 3))
        spacing_waves = self.spacing / 3
        new_head_pos = [self.head_position[0], self.head_position[1] - spacing_waves, self.head_position[2]]

        ####################2nd WAVE###########################################
        for l in range(0, nbl):
            left_side2[l][0], left_side2[l][1], left_side2[l][2] = new_head_pos[0] - (l + 1) * x_dist, \
                                                                new_head_pos[1] - (
                                                                        l + 1) * y_dist, new_head_pos[2]
            point1 = left_side2[l]
            drl = Drone(point1, l,0 )
            self.drone_list.append(drl)
        self.drone_list.append(new_head_pos)
        for r in range(0, nbr):
            right_side2[r][0], right_side2[r][1], right_side2[r][2] = new_head_pos[0] + (r + 1) * x_dist, \
                                                                   new_head_pos[1] - (
                                                                           r + 1) * y_dist, new_head_pos[2]
            point2 = right_side2[r]
            drr = Drone(point2, r + nbl, 0)
            self.drone_list.append(drr)
        pos2 = np.vstack((np.vstack((np.array(new_head_pos), left_side2)), right_side2))

        final_pos = np.vstack((pos1, pos2))
        return final_pos



### Ball formation class ###
class Ball :

    def __init__(self,number_drones, diameter, center, spacing):
        self.diameter = diameter                                                # Define the diameter of the ball.
        self.center = center                                                    # Define the center of the ball.
        self.spacing = spacing                                                  # Define the space between each drone.
        self.number_drones = number_drones                                      # Define the number of drone.
        self.drone_list = []
        self.get_ini_pos_ball()

### Function to get the initial positions of each drone in the swarm in a ball formation ###
    def get_ini_pos_ball(self):
        surface_points = []
        phi = np.pi * (3. - np.sqrt(5.))
        for i in range(int(self.number_drones*0.5)):
            y = 1 - (i / float(self.number_drones*0.5 - 1)) * 2
            radius_at_height = np.sqrt(1 - y**2) * self.diameter/2
            theta = phi * i
            x = np.cos(theta) * radius_at_height
            z = np.sin(theta) * radius_at_height
            point = self.center + np.array([x, y * self.diameter/2, z])
            dr = Drone(point, i,0)
            self.drone_list.append(dr)
            surface_points.append(point)
        internal_points = []
        num_internal_per_layer = ceil(self.diameter/2 / self.spacing)
        for r in range(int(self.number_drones*0.5)):
            layer = r % num_internal_per_layer
            height = layer * self.spacing + self.spacing / 2
            theta = np.random.uniform(0, 2*np.pi)
            phi = np.arccos(2*np.random.uniform(0, 1) - 1)
            x = self.center[0] + height * np.sin(phi) * np.cos(theta)
            y = self.center[1] + height * np.sin(phi) * np.sin(theta)
            z = self.center[2] + height * np.cos(phi)
            point = np.array([x, y, z])
            de = Drone(point, r+int(self.number_drones*0.5), 0)
            self.drone_list.append(de)
            internal_points.append(point)
        drones_to_be_dangerous = []
        for k in range (int((1/3)*len(self.drone_list))) :
            drones_to_be_dangerous.append(self.drone_list[k])

        for drone in drones_to_be_dangerous :
            drone.damage = 1


        return np.vstack((internal_points,surface_points))


### Line formation class ###
class Line (Drone):
    def __init__(self, number_drones, center, spacing, direction):
        self.number_drones = number_drones                                      # Define the central position of the line formation.
        self.center = center                                                    # Define the central drone's position.
        self.spacing = spacing                                                  # Define the space between each drone.
        self.direction = direction                                              # Define the moving direction of the line formation.
        self.drone_list = []
        self.get_init_pos_front()


### Function to get the initial positions of each drone in the swarm in a line formation ###
    def get_init_pos_front(self):
        initial_positions = []
        for i in range(self.number_drones):
            position = np.array(self.center) + np.array(self.direction) * i * self.spacing
            drone = Drone(position, i,0)
            self.drone_list.append(drone)
            initial_positions.append(drone.pos)



### Random formation class ###
class Random (Drone):
    def __init__(self, number_drones, distance_to_base):
        self.number_drones = number_drones
        self.drone_list = []
        self.distance_to_base = distance_to_base
        self.get_ini_pos_random()

### Function to get the initial positions of each drone in the swarm in a line formation ###
    def get_ini_pos_random(self):
        positions = np.random.randint(30, 45, size=(self.number_drones, 3))
        for k in range(int((2/3)*len(positions))):
            drone = Drone(positions[k], k, 0)
            self.drone_list.append(drone)
        for d in range(int((2/3)*len(positions)), len(positions)):
            dangerous_drone = Drone(positions[d], d, 0)
            dangerous_drone.damage = 2
            self.drone_list.append(dangerous_drone)



