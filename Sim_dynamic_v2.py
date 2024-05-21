from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np
from Drone import Drone
from Value_function import Feed_MIP

"This version of the dynamic algorithm is made so that the engagement zone variable is now "
"in the value function as a product with an indicator function (E_r =1 if target i is in range of "
"weapon j and E_r= 0 otherwise"

class Sim_dynamic_v2:

    def __init__(self, st , time_step, base, weights):
        self.st = st  # End time in simulation
        self.nbd = len(base.drone_list)  # Number of drones
        self.time_step = time_step  # period of time for the assignment
        self.drone_list = base.drone_list  # take from GBAD the drone list, it contains, position, index..
        self.base = base
        self.n = len(base.weapons)  # number of weapons
        self.assignment = None  # initialize the assignment at nothing at the beginning of the simulation
        self.downtime_timer = 0  # Counter in order to measure if weapon is available regarding its downtime
        self.counter_drones_destroyed = 0
        self.the_time_steps = []
        self.weapons_with_ammo = []
        self.targets_alive_ts = []
        self.GBAD_health_state = []
        self.nbd_drones_escaped = []
        self.surv_weapons = {'Gun1': [], 'Gun2': [], 'Grenade1': [], 'Laser1': []}
        self.theo_damage = []
        self.weights = weights
        self.score = 0
        self.time_to_kill_everybody = None
        self.drones_assigned= []


    def simu_dynamic_v2(self):
        for weap in self.base.weapons:
            for drone in self.base.drone_list:
                self.surv_weapons[f'{weap.name}'].append(1 - weap.Pc)
        print(f'Surv prob for all weapons and drones : {self.surv_weapons}')
        for t in range (0, self.st, self.time_step) :
            print(f'Time Step = {t}')
            self.the_time_steps.append(t)
            self.GBAD_health_state.append(self.base.health)

            self.weapons_with_ammo = []
            for weapon in self.base.weapons:

                if weapon.ammunition > 0:
                    self.weapons_with_ammo.append(weapon)
            w_prob = [w.Pc for w in self.weapons_with_ammo]
            if len(w_prob) == 0:
                print('All the weapons are out of ammunitions ')
                break
            ## Define the reward matrix with all the value_function values
            drones_alive = [drone for drone in self.base.drone_list if drone.active ==1]

            # print(f'Length of drones_alive is : {len(drones_alive)}')
            reward_matrix = np.reshape(np.repeat([1]*len(self.weapons_with_ammo),len(drones_alive)), (len(self.weapons_with_ammo), -1))
            reward_matrix = reward_matrix.astype(float)
            feed_mip = Feed_MIP(self.weapons_with_ammo, drones_alive, self.base, self.weights)
            # print(f'time step = {t} and beta = {feed_mip.dynamic_weights[1]}')

            dist = [np.linalg.norm(np.array([0, 0, 0]) - drone.pos) for drone in drones_alive]
            if len(dist) != 0:
                self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
                ### Normalize the value to calculate the value function
                max_dist, min_dist = max(dist), min(dist)
                for drone in drones_alive:
                    number_of_weapons_inrange = 0
                    drone.drone_dist = (np.linalg.norm(drone.pos - np.array([0, 0, 0])) - min_dist + 0.1)/(max_dist - min_dist+ 0.1)
                    for weapon in self.weapons_with_ammo:
                        if weapon.range_window[0] <= np.linalg.norm(drone.pos - np.array([0, 0, 0])) <= \
                                weapon.range_window[1]:  ### if that drone is in range of that weapon
                            number_of_weapons_inrange += 1

                    drone.engagement_zone = number_of_weapons_inrange / len(self.weapons_with_ammo)
                # print(f'Engagement zone values :{[drone.engagement_zone for drone in drones_alive]}')


                for index, w in enumerate(self.weapons_with_ammo):
                    reward_matrix[index] = reward_matrix[index] * [feed_mip.get_value_function_v2(drone, w, self) for drone in drones_alive]
                    reward_matrix[index] = reward_matrix[index] * [w.range_window[0] <= distance <= w.range_window[1] for distance in dist]

                    if np.mod(self.downtime_timer, w.downtime) != 0:  ## check if  weapon is ready and re-loading.
                        print(f' {w.name} is not available')
                        reward_matrix[index] = [0] * len(self.base.get_distance_drone(self.base))
                # print(f'Reward_matrix = {reward_matrix}')
                self.assignment = MIP_Assignment(reward_matrix, self.weapons_with_ammo, drones_alive)
                # print(f'The assignment is : {self.assignment.assignement}')
                # print(f'Drones in drones_alive = {[drone.idx for drone in drones_alive]}')
                # print(f'drones indexes assigned = {[i[1] for i in self.assignment.assignement]}')
                self.drones_assigned.append(self.assignment.assignement)
                print(f'drones assigned : {self.drones_assigned}')
                for i in self.assignment.assignement:

                    drones_alive[i[1]].drone_get_destroyed(drones_alive[i[1]], self.weapons_with_ammo[i[0]], self.base, self)

                ### Need to update the GBAD_Health and calculating the theoritical damage to the base
                sum_damage = 0
                self.nbd_drones_escaped.append(len([i for i in self.drone_list if i.drone_escaped == True]))
                for drone in self.base.drone_list:

                    if drone.active == 1:
                        drone.update_drone_pos(self.time_step)
                        sum_damage += drone.damage
                    for weapon in self.weapons_with_ammo:
                        drone.drone_escape(weapon, self.base)
                self.theo_damage.append(sum_damage)
            else:
                self.time_to_kill_everybody = t
                self.targets_alive_ts.append(0)
                self.theo_damage.append(self.theo_damage[-1])
                self.nbd_drones_escaped.append(self.nbd_drones_escaped[-1])
        return self.counter_drones_destroyed, self.score


###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####


## Get the weapons ###
Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
range_sup_weapons = [Gun1.range_window[1], Gun2.range_window[1], grenade1.range_window[1], Laser1.range_window[1]]
range_min = min(range_sup_weapons)

weigths = [4, 2, 1, 2, 1.75]
### Get the initial swarm and all initialize the base ###
n = 4                 # number of weapons #
### generating 30 random positions

random_swarm = Random(30, range_min)
base = GBAD(np.array([0, 0, 0]), random_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])



## Run the simulation ##

sim3 = Sim_dynamic_v2(30, 1, base, weigths)
number_of_drones_destroyed = sim3.simu_dynamic_v2()[0]
