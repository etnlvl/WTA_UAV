from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import matplotlib.pyplot as plt
import Weapons
import numpy as np
from Drone import Drone
from Value_function import Feed_MIP

class Sim_dynamic:

    def __init__(self, st, time_step, base, weights):
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
        self.nbd_drones_escaped = []
        self.weights = weights
        self.score = 0
        self.time_to_kill_everybody = None
        self.list_of_variables = {'Gun1': [], 'Gun2' : [], 'Grenade1' : [], 'Laser1' : [] }
        self.surv_weapons = {'Gun1': [], 'Gun2': [], 'Grenade1': [], 'Laser1': []}
    def simu_dynamic(self):
        dist2 = {drone: np.linalg.norm(np.array([0, 0, 0]) - drone.pos) for drone in self.drone_list}
        furthest_drone = max(dist2, key=dist2.get)
        for weap in self.base.weapons:
            for drone in self.base.drone_list:
                self.surv_weapons[f'{weap.name}'].append(1 - weap.Pc)
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
                break
            ## Define the reward matrix with all the value_function values
            drones_alive = [drone for drone in self.base.drone_list if drone.active ==1]
            reward_matrix = np.reshape(np.repeat([1]*len(self.weapons_with_ammo),len(drones_alive)), (len(self.weapons_with_ammo), -1))
            feed_mip = Feed_MIP(self.weapons_with_ammo, drones_alive, self.base, self.weights)
            reward_matrix = reward_matrix.astype(float)
            dist = [np.linalg.norm(np.array([0, 0, 0]) - drone.pos) for drone in drones_alive]
            print(f'Type of furthest drone variable : {type(furthest_drone)}')
            if len(dist) != 0:
                self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
                ### Normalize the value to calculate the value function
                max_dist, min_dist = max(dist), min(dist)
                ### Set the engagement zone   ### next step is to set up this variable as an indicator function which is equal
                ### to one if it's in range of the weapon or 0 if it's not
                for drone in drones_alive:
                    number_of_weapons_inrange = 0
                    drone.drone_dist = (np.linalg.norm(drone.pos - np.array([0, 0, 0])) - min_dist + 0.1) / (
                                max_dist - min_dist + 0.1)
                    for weapon in self.weapons_with_ammo:
                        if weapon.range_window[0] <= np.linalg.norm(drone.pos - np.array([0, 0, 0])) <= weapon.range_window[1]:             ### if that drone is in range of that weapon
                            number_of_weapons_inrange += 1


                    drone.engagement_zone = number_of_weapons_inrange/len(self.weapons_with_ammo)

                for index, w in enumerate(self.weapons_with_ammo):

                    print(f'For weapon : {w.name}')
                    reward_matrix[index] = [feed_mip.get_value_function_v1(drone, w, self)[0] for drone in drones_alive]
                    # print(f'For Weapon {w.name} at time step ={t}, value functions of drones are : {reward_matrix[index]}')
                    reward_matrix[index] = reward_matrix[index] * [w.range_window[0] <= distance <= w.range_window[1] for distance in dist]
                    self.list_of_variables[f'{w.name}'].append(np.array(feed_mip.get_value_function_v1(furthest_drone, w, self)[1:]))

                print(f' Reward_matrix to feed the MIP = {reward_matrix}')
                self.assignment = MIP_Assignment(reward_matrix, self.weapons_with_ammo, drones_alive)
                for i in self.assignment.assignement:

                    drones_alive[i[1]].drone_get_destroyed(drones_alive[i[1]], self.weapons_with_ammo[i[0]], self.base, self)

                ### Need to update the GBAD_Health and calculate the theorical damage to the base
                sum_damage = 0
                self.nbd_drones_escaped.append(len([i for i in self.drone_list if i.drone_escaped == True]))
                for drone in self.base.drone_list:
                    if drone.active == 1:
                        drone.update_drone_pos(float(self.time_step))
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

#
# Get the weapons ###
# Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
# Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
# grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
# Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
# Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
# range_sup_weapons = [Gun1.range_window[1], Gun2.range_window[1], grenade1.range_window[1], Laser1.range_window[1]]
# range_min = min(range_sup_weapons)
# weigths = [4, 2, 1, 2, 1.75]
# ### Get the initial swarm and all initialize the base ###
# n = 4                 # number of weapons #
# ### generating 30 random positions
# print(f'range_max = {range_min}')
# random_swarm = Random(30, range_min)
# base = GBAD(np.array([0, 0, 0]), random_swarm.drone_list, [Gun1, Gun2, grenade1,
#                                                                      Laser1])
# ## Run the simulation ##
#
# sim3 = Sim_dynamic(30, 1, base, weigths)
# number_of_drones_destroyed = sim3.simu_dynamic()[0]
# results_variables = sim3.list_of_variables
# print(f'List of variables for the furthest drone at the beginning : {results_variables}')
# print(f' for the gun and furthest_drone : {results_variables['Gun1']}')
# print(f' size of it : {len(results_variables['Gun1'])}')
# print(f' Survivavibility : {sim3.surv_weapons}')
# Sr_gun1 = []
# Gr_gun1 = []
# Er_gun1 = []
# Dr_gun1 = []
# Dir_gun1 = []
# Sr_gun2 = []
# Gr_gun2 = []
# Er_gun2 = []
# Dr_gun2 = []
# Dir_gun2 = []
#
# Sr_grenade1, Er_grenade1, Dr_grenade1, Dir_grenade1 = [], [], [], []
#
# Sr_laser1, Er_laser1, Dr_laser1, Dir_laser1 = [], [], [], []
#
#
# for values in results_variables['Gun1']:
#     Sr_gun1.append(values[0])
#     Er_gun1.append(values[2])
#     Dr_gun1.append(values[3])
#     Dir_gun1.append(values[4])
#
#
# for values in results_variables['Gun2']:
#     Sr_gun2.append(values[0])
#     Er_gun2.append(values[2])
#     Dr_gun2.append(values[3])
#     Dir_gun2.append(values[4])
#
#
# for values in results_variables['Grenade1']:
#     Sr_grenade1.append(values[0])
#     Er_grenade1.append(values[2])
#     Dr_grenade1.append(values[3])
#     Dir_grenade1.append(values[4])
#
#
# for values in results_variables['Laser1']:
#     Sr_laser1.append(values[0])
#     Er_laser1.append(values[2])
#     Dr_laser1.append(values[3])
#     Dir_laser1.append(values[4])
#
#
# fig, axs = plt.subplots(4, figsize=(10,8))
# print(f'Sr_gun1 : {Sr_gun1}')
# axs[0].set_title('Gun1')
# axs[0].plot(Sr_gun1, color ='r')
# axs[0].plot(Er_gun1, color = 'b')
# axs[0].plot(Dr_gun1, color ='black')
# axs[0].plot(Dir_gun1, color ='green')
#
# axs[1].set_title('Gun2')
# axs[1].plot(Sr_gun2,color ='r')
# axs[1].plot(Er_gun2, color = 'b')
# axs[1].plot(Dr_gun2,color ='black')
# axs[1].plot(Dir_gun2, color ='green')
#
# axs[2].set_title('Grenade1')
# axs[2].plot(Sr_grenade1, color ='r')
# axs[2].plot(Er_grenade1, color = 'b')
# axs[2].plot(Dr_grenade1, color ='black')
# axs[2].plot(Dir_grenade1, color ='green')
#
# axs[3].set_title('Laser1')
# axs[3].plot(Sr_laser1, color ='r')
# axs[3].plot(Er_laser1, color = 'b')
# axs[3].plot(Dr_laser1, color ='black')
# axs[3].plot(Dir_laser1, color ='green')
# axs[0].set_ylim(0.0, 1.1)
# axs[1].set_ylim(0.0, 1.1)
# axs[2].set_ylim(0.0, 1.1)
# axs[3].set_ylim(0.0, 1.1)
# plt.show()


# print(f'results variables = {results_variables}')
# print(f' for gun1, results variables = {results_variables['Gun1']}')
# for array in results_variables['Gun1']:
#     for drone
# for key, value in results_variables.items():
#     # print(len(value))
#     Sr = [value[0][0][4] for i in results_variables[key]]
#     plt.plot([value[0][0][4] for i in results_variables[key]])
#     plt.show()
# print(Sr)
# # print(value)



#
# # for i in results_variables['Gun1']:
# #     Sr.append(i[0][0])
#     # Gr.append(i[0][1])
# print(Sr)
#
# plt.plot(Sr)
# # plt.plot(Gr)
# plt.show()

# ax, fig = plt.subplot()
#     ax.plot(Sr)





# print(f'number of drones destroyed = {number_of_drones_destroyed}')


