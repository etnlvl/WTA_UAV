import numpy as np
import matplotlib.pyplot as plt
import Weapons
import numpy as np
from math import *
import Weapons
from gbad import GBAD


class Drone:
    def __init__(self, pos, idx, close_drone=None):
        self.active = 1   # says if the drone is still in state of function
        self.close_drone = close_drone
        self.pos = pos
        self.idx = idx
        self.threat_val = 1     #~ the threat value will increase as the
                                        #distance to the base decrease.
        self.speed = np.array([-3,-1,-2])    # ~100km/h
        self.drone_dist = 0.60
        self.damage = 0.80 #0.2
        self.target_survivability = 0.70
        self.engagement_zone = 0.60



    def drone_get_destroyed(self, drone, weapon, base, simu):
        if weapon.ammunition > 0:
            if np.random.rand() < weapon.Pc:  #### It means that the drone has been hit so the active value of it is then updated to 0.
                ## we make the assumption that if the drone is reached, it is destroyed
                print(f'Drone {drone.idx} has been destroyed by : {weapon.name}')


                if drone.active == 1:
                    simu.counter_drones_destroyed += 1
                    simu.score += drone.threat_val
                drone.active = 0
                # base.drone_list.remove(drone)
                return True
            else:  #### The drone will not be hit at this time step, so we need to upgrade the threat value.

                drone.target_survivability += 0.045
                drone.engagement_zone += 0.02
                print(f'Drone {drone.idx} has been missed by : {weapon.name}')
                return False
        else :
            print(f'{weapon.name} is out of ammunition')
        weapon.ammunition += -1

    def drone_get_check(self, weapon):
        if weapon.ammunition > 0:
            if np.random.rand() < weapon.Pc:  #### It means that the drone has been hit so the active value of it is then updated to 0.
                ## we make the assumption that if the drone is reached, it is destroyed
                return True
            else:  #### The drone will not be hit at this time step, so we need to upgrade the threat value.
                return False
        else:
            print(f'{weapon.name} is out of ammunition')



    def drone_get_remove(self, weapon):
        if np.random.rand() < weapon.Pc:
            return True
        else:
            return False


    def drone_escape(self, weapon, base):
        if np.linalg.norm(self.pos - np.array([0, 0, 0])) < weapon.range_window[0]:
            answer = True
            print(f'drone_escape range of {weapon.name} ')
            base.health -= 0.01 # self.damage
        else :
            answer = False
        return answer



    def update_drone_pos(self, time):  #### Update the position of the drone
        self.pos += self.speed * time
        self.drone_dist += 0.01
        # self.threat_val += 1

    def update_TV(self):
        pos_base = np.array([0, 0, 0])
        distance_of_drone = np.linalg.norm(self.pos - pos_base)
        threat_val = 1/distance_of_drone
        self.threat_val = threat_val
        return self.threat_val



        #








#### To get all the initial position of the swarm in the desired formation ####

# To get a wave formation #
class Wave :
    def __init__(self,number_drones, head_position, angle, spacing):
        self.head_position = head_position
        self.angle = angle
        self.spacing = spacing
        self.number_drones = number_drones
        self.drone_list = []

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
        self.drone_list.append(self.head_position)
        for r in range(0, nbr):
            right_side[r][0], right_side[r][1], right_side[r][2] = self.head_position[0] + (r + 1) * x_dist, self.head_position[1] - (
                        r + 1) * y_dist, self.head_position[2]
            point2 = right_side[r]
            drr = Drone(point2, r+nbl, 0)
            self.drone_list.append(drr)
        pos = np.vstack((np.vstack((np.array(self.head_position), left_side)), right_side))   # joining the 2 sequences, left side and right side

        return pos

        # To get a double wave formation #
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



# To get a ball formation #
class Ball :

    def __init__(self,number_drones, diameter, center, spacing):
        self.diameter = diameter
        self.center = center
        self.spacing = spacing
        self.number_drones = number_drones
        self.drone_list = []
        self.get_ini_pos_ball()

    def get_ini_pos_ball(self):
        surface_points = []
        phi = np.pi * (3. - np.sqrt(5.))
        for i in range(int(self.number_drones*0.5)):           # creating the points at the surface of the ball
            y = 1 - (i / float(self.number_drones*0.5 - 1)) * 2
            radius_at_height = np.sqrt(1 - y**2) * self.diameter/2
            theta = phi * i
            x = np.cos(theta) * radius_at_height
            z = np.sin(theta) * radius_at_height
            point = self.center + np.array([x, y * self.diameter/2, z])
            dr = Drone(point, i,0)
            # dr.survivability =
            self.drone_list.append(dr)
            surface_points.append(point)
        internal_points = []
        num_internal_per_layer = ceil(self.diameter/2 / self.spacing)
        for r in range(int(self.number_drones*0.5)):            # creating the points inside the ball
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

        return np.vstack((internal_points,surface_points))


# To get a front formation #
class Front (Drone):
    def __init__(self, number_drones, center, spacing, direction):
        self.number_drones = number_drones
        self.center = center
        self.spacing = spacing
        self.direction = direction
        self.drone_list = []

    def get_init_pos_front(self):
        initial_positions = []
        for i in range(self.number_drones):
            position = np.array(self.center) + np.array(self.direction) * i * self.spacing
            drone = Drone(position, i,0)  # Create a Drone instance with position, index and value_objective
            self.drone_list.append(drone)  # Add the drone to the list of drones
            initial_positions.append(drone.pos)  # Append index and position tuple
            print(initial_positions)
        return initial_positions


class Random (Drone):
    def __init__(self, number_drones):
        self.number_drones = number_drones
        self.drone_list = []
        self.get_ini_pos_random()

    def get_ini_pos_random(self):
        positions = np.random.randint(35, 55, size=(self.number_drones, 3))
        for k in range(20):
            drone = Drone(positions[k], k, 0)
            self.drone_list.append(drone)
        for d in range(20, 30):
            dangerous_drone = Drone(positions[d], d, 0)
            dangerous_drone.damage = 1
            self.drone_list.append(dangerous_drone)



