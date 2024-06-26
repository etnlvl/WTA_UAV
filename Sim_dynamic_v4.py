from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
from Drone import Line
import Weapons
import numpy as np
from Drone import Drone
import statistics
from Value_function import Feed_MIP
import matplotlib.pyplot as plt
### The goal of this version is to have dynamics factors so
### the evolution of the variables are not always done with the same threshold
class Sim_dynamic_v4:

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
        self.nbd_drones_escaped = []
        self.weights = weights
        self.score = 0
        self.time_to_kill_everybody = None
        self.surv_weapons = {'Gun1': [], 'Gun2': [], 'Grenade1': [], 'Laser1': []}


    def simu_dynamic_v4(self):
        for weap in self.base.weapons:
            for drone in self.base.drone_list:
                self.surv_weapons[f'{weap.name}'].append(1 - weap.Pc)
        for t in range (0, self.st, self.time_step) :
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
            drones_alive = [drone for drone in self.base.drone_list if drone.active ==1 ]
            reward_matrix = np.reshape(np.repeat([1]*len(self.weapons_with_ammo),len(drones_alive)), (len(self.weapons_with_ammo), -1))
            reward_matrix = reward_matrix.astype(float)
            feed_mip = Feed_MIP(self.weapons_with_ammo, drones_alive, self.base, self.weights)
            dist = [np.linalg.norm(np.array([0, 0, 0]) - drone.pos) for drone in drones_alive]
            print(f'GBAD state = {self.GBAD_health_state[-1]}')
            if len(dist) != 0:

                self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
                ### Normalize the value to calculate the value function
                max_dist, min_dist = max(dist), min(dist)
                for index, w in enumerate(self.weapons_with_ammo):
                    for drone in drones_alive:
                        self.weights[4] = drone.get_lambda(w, self.base)
                        self.weights[1] = drone.get_beta(self.base)
                        self.weights[0] = drone.get_alpha(8, t)

                        drone.drone_dist = (np.linalg.norm(drone.pos - np.array([0, 0, 0])) - min_dist + 0.1) / (
                                    max_dist - min_dist + 0.1)
                        if w.range_window[0] <= np.linalg.norm(drone.pos - np.array([0, 0, 0])) <= w.range_window[1]:         ### if that drone is in range of that weapon
                            position = drone.pos
                            drone.engagement_zone = 1
                        else:
                            drone.engagement_zone = 0

                    reward_matrix[index] = reward_matrix[index] * [feed_mip.get_value_function_v1(drone, w, self)[0] for drone in drones_alive]
                    reward_matrix[index] = reward_matrix[index] * [w.range_window[0] <= distance <= w.range_window[1] for distance in dist]

                self.assignment = MIP_Assignment(reward_matrix, self.weapons_with_ammo, drones_alive)
                for i in self.assignment.assignement:

                    drones_alive[i[1]].drone_get_destroyed(drones_alive[i[1]], self.weapons_with_ammo[i[0]], self.base, self)

                ### Need to update the GBAD_Health and calculating the theoretical damage to the base
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

###
## Get the weapons ###
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
# random_swarm = Random(100, range_min)
#
# base = GBAD(np.array([0, 0, 0]), random_swarm.drone_list, [Gun1, Gun2, grenade1,
#                                                                      Laser1])
# print(f'Drone threat values = {[drone.threat_val for drone in random_swarm.drone_list]}')
#
#
# ## Run the simulation ##
#
# sim4 = Sim_dynamic_v4(60, 1, base, weigths)
# number_of_drones_destroyed = sim4.simu_dynamic_v4()[0]
#
target_alive = []
gbad = []
damage_cap = []
score_of_simu = []
nb_simulations = 10
def average_results(results):
    new_lists = [[] for _ in range(len(results[0]))]
    # Parcourir chaque sous-liste et ajouter les éléments aux nouvelles listes
    for sublist in results:
        for i, elem in enumerate(sublist):
            new_lists[i].append(elem)
    avg_list = []
    # Afficher les nouvelles listes
    for lst in new_lists:
        avg_list.append(statistics.mean(lst))
    return avg_list


#
fig, axs = plt.subplots(2,1, figsize=(9, 7))

for k in range(nb_simulations) :
    Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
    Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
    grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
    Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
    Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
    swarm = Line(100, np.array([30, 35, 40]),0.58, np.array([-1, -0.5, 0]))
    base = GBAD(np.array([0, 0, 0]), swarm.drone_list, [Gun1, Gun2, grenade1,
                                                               Laser1])
    simu = Sim_dynamic_v4(60, 1, base, [4, 1, 2, 1, 1.75])
    simu.simu_dynamic_v4()
    # print(f'targets alive : {simu.targets_alive_ts}')
    # axs[0].plot(simu.targets_alive_ts, linewidth='1', linestyle='--')
    # axs[0].set_xlabel('Time in s')
    # axs[0].set_ylabel('Number of drones alive')
    axs[0].plot(simu.GBAD_health_state, linewidth='1', linestyle ='--')
    axs[0].set_xlabel('Time in s')
    axs[0].set_ylabel('GBAD Health')
    # axs[1].plot(simu.theo_damage, linewidth='1', linestyle ='--')
    # axs[1].set_xlabel('Time in s')
    # axs[1].set_ylabel('GBAD health')
    target_alive.append(simu.targets_alive_ts)
    gbad.append(simu.GBAD_health_state)
    damage_cap.append(simu.theo_damage)
    score_of_simu.append(simu.score)

average_targets_alive = average_results(target_alive)
average_health = average_results(gbad)
average_damage = average_results(damage_cap)
# axs[1].plot(score_of_simu, linewidth ='3', linestyle= '-', color='black')
# axs[0].plot(average_targets_alive, linewidth ='3', linestyle= '-', color='black')
# axs[1].plot(average_damage, linewidth ='3', linestyle= '-', color='black')
# axs[1].set_xlabel('Time in s ')
# axs[1].set_ylabel('Damage capability')
axs[0].plot(average_health, linewidth ='3', linestyle= '-', color='black')

axs[1].set_ylim(50,105)
# axs[1].sharey(axs[0])
axs[1].plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], score_of_simu, "-gs")
# axs[1].set_ylim(85,110)
axs[1].set_xlabel('Time in s ')
axs[1].set_ylabel('Score')
# axs[1].plot(average_damage, linewidth='3', linestyle ='-', color='black')

plt.show()