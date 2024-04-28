from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np
from Drone import Drone
from Value_function import Feed_MIP
### The goal of this version is to have dynamics factors so
### the evolution of the variables are not always done with the same threshold
class Sim_dynamic_v3:

    def __init__(self, st , time_step, base, weights) :
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
        self.theo_damage = []
        self.weights = weights
        self.score = 0
        self.time_to_kill_everybody = None


    def simu_dynamic_v2(self):
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
            drones_alive = [drone for drone in self.base.drone_list if drone.active ==1 ]

            print(f'Length of drones_alive is : {len(drones_alive)}')
            reward_matrix = np.reshape(np.repeat([1]*len(self.weapons_with_ammo),len(drones_alive)), (len(self.weapons_with_ammo), -1))
            feed_mip = Feed_MIP(self.weapons_with_ammo, drones_alive, self.base, self.weights)
            if t == int((3 / 5) * self.st):
                feed_mip.weights[1] += 5
            dist = [np.linalg.norm(np.array([0, 0, 0]) - drone.pos) for drone in drones_alive]
            if len(dist) != 0:
                self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
                ### Normalize the value to calculate the value function
                max_dist = max(dist)
                min_dist = min(dist)
                for drone in drones_alive:
                    drone.drone_dist = (np.linalg.norm(drone.pos - np.array([0, 0, 0])) - min_dist + 0.1)/(max_dist - min_dist+ 0.1)
                print(f'the weapons with ammo at this time_step are : {self.weapons_with_ammo}')
                ### Set the engagement zone version 2 with the indicator function

                for index, w in enumerate(self.weapons_with_ammo):
                    for drone in drones_alive:
                        if w.range_window[0] <= np.linalg.norm(drone.pos - np.array([0, 0, 0])) <= w.range_window[1]:
                            drone.engagement_zone = 1
                        else:
                            drone.engagement_zone = 0

                    print(f'reward_matrix[index] ={reward_matrix[index]}')
                    print(f'length of drones_alive = {len(drones_alive)}')
                    print(f'length of dist= {len(dist)}')
                    reward_matrix[index] = reward_matrix[index] * [feed_mip.get_value_function(drone) for drone in drones_alive]
                    reward_matrix[index] = reward_matrix[index] * [w.range_window[0] <= distance <= w.range_window[1] for distance in dist]

                    if np.mod(self.downtime_timer, w.downtime) != 0:  ## check if  weapon is ready and re-loading.
                        print(f' {w.name} is not available')
                        reward_matrix[index] = [0] * len(self.base.get_distance_drone(self.base))
                print(f'Reward_matrix at this time step t={t} is {reward_matrix}')
                print(f'Weapons with ammos = {self.weapons_with_ammo}')
                self.assignment = MIP_Assignment(reward_matrix, self.weapons_with_ammo, drones_alive)
                print(f'The assignment is : {self.assignment.assignement}')
                print(f'Drones in drones_alive = {[drone.idx for drone in drones_alive]}')
                print(f'drones indexes assigned = {[i[1] for i in self.assignment.assignement]}')
                for i in self.assignment.assignement:

                    drones_alive[i[1]].drone_get_destroyed(drones_alive[i[1]], self.weapons_with_ammo[i[0]], self.base, self)

                ### Need to update the GBAD_Health and calculating the theoritical damage to the base
                sum_damage = 0
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
        return self.counter_drones_destroyed, self.score


###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####


## Get the weapons ###
# Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
# Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
# grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
# Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
# Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
# weigths = [4, 2, 1, 0.5, 0.5]
# ### Get the initial swarm and all initialize the base ###
# n = 4                 # number of weapons #
# ### generating 30 random positions
#
# random_swarm = Random(30)
# base = GBAD(np.array([0, 0, 0]), random_swarm.drone_list, [Gun1, Gun2, grenade1,
#                                                                      Laser1])
# print(f'Drone threat values = {[drone.threat_val for drone in random_swarm.drone_list]}')
#
#
# ## Run the simulation ##
#
# sim3 = Sim_dynamic_v2(20, 1, base, weigths)
# number_of_drones_destroyed = sim3.simu_dynamic_v2()[0]
# print(f'GBAD health at each time step : {sim3.GBAD_health_state}')
# print(f'Results for the following weights: '
#       f'alpha(Target survivability)= {sim3.weights[0]}, '
#       f'beta(GBAD health)={sim3.weights[1]}, '
#       f'gamma(Engagement zone) ={sim3.weights[2]}, '
#       f'phi(Target Damage)={sim3.weights[3]}, '
#       f'lambda(Target distance)={sim3.weights[4]}')
# print('*************')
# print(f'GBAD HEALTH = {base.health}')
# print(f'SCORE = {sim3.score}')
# print(f'DRONES DESTROYED = {number_of_drones_destroyed}')
# print('*************')
# print(f'Time to kill all drones = {sim3.time_to_kill_everybody} s.')
#
#
# print(f'For the stats : the time steps = {sim3.the_time_steps} , number_of_targets_alive = {sim3.targets_alive_ts}')
# print(f'Theoritical damage :{sim3.theo_damage}')
