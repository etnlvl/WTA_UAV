from Drone import Random
from Sim_dynamic import Sim_dynamic
from Sim_dynamic_v2 import Sim_dynamic_v2
from Sim_dynamic_v4 import Sim_dynamic_v4
from Sim_dynamic_v3 import Sim_dynamic_v3
from MIP_for_comparaison import Sim2
from MIP_Assignment import MIP_Assignment
import matplotlib.pyplot as plt
from gbad import GBAD
import Weapons
import numpy as np
from math import *
import statistics
from scipy.optimize import curve_fit
"This file runs several simulations and compare each other in order to see the main differences of performance."
class Stats :
    def __init__(self, number_of_drones, st, time_step, weapons_desired, nb_sim):
        self.number_of_drones = number_of_drones
        self.st = st
        self.time_step = time_step
        self.weapons_desired = weapons_desired        # {'Gun': [nb_items, nb_ammo], 'Grenade' : [nb_items, nb_ammo], 'Laser': [nb_items, nb_ammo]}
        self.nb_sim = nb_sim
        self.total_nb_alive = []
        self.weapons_list = []
        self.alive_along_simulation_MIP = []   ### [[30,27,26,23,20,20,16,,15,13,10,9,7,6,4,2,1],[30,27,26,23,20,20,16,,15,13,10,9,7,6,4,2,1]] example for 2 simulations
        self.alive_along_simulation_Dynamic = []
        self.alive_along_simulation_Dynamic_v2 = []
        self.alive_along_simulation_Dynamic_v3 = []
        self.scores_for_simulations_MIP = []
        self.score_for_simulation_Dynamic = []
        self.score_for_simulation_Dynamic_v2 = []
        self.score_for_simulation_Dynamic_v3 = []
        self.GBAD_health_MIP = []
        self.GBAD_health_Dynamic = []
        self.GBAD_health_Dynamic_v2 = []
        self.GBAD_health_Dynamic_v3 = []
        self.time_to_kill_everybody_MIP = []
        self.time_to_kill_everybody_Dynamic = []
        self.damage_MIP = []
        self.damage_Dynamic = []
        self.damage_Dynamic_v2 = []
        self.damage_Dynamic_v3 = []
        self.nbd_drones_escaped_MIP = []
        self.nbd_drones_escaped_Dynamic = []
        self.nbd_drones_escaped_Dynamic_v2 = []
        self.nbd_drones_escaped_Dynamic_v3 = []

        self.the_time_steps = []

    def statistic(self):

        for k in range(self.nb_sim):

            ####************************************#######
            ####************************************#######
            ####   ELEMENTS FOR THE MIP             #######
            ### Create the weapons, the base and the targets for each simulation
            Gun1_MIP = Weapons.Gun('Gun1', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            Gun2_MIP = Weapons.Gun('Gun2', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            grenade1_MIP = Weapons.Grenade('Grenade1', 50, np.array([False, False]), self.weapons_desired['Grenade'][1])
            Laser1_MIP = Weapons.Laser('Laser1', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            weapons_list1 = [Gun1_MIP, Gun2_MIP, grenade1_MIP, Laser1_MIP]
            random_swarm1 = Random(self.number_of_drones, 60 )
            print(f'Distance to base : {[np.linalg.norm(d.pos) for d in random_swarm1.drone_list]}')
            base1 = GBAD(np.array([0, 0, 0]), random_swarm1.drone_list, weapons_list1)
            ### Proceeding all the MIP simulations
            simu_MIP = Sim2(self.st, self.time_step, base1)
            number_of_drones_destroyed_MIP = simu_MIP.next()[0]
            self.alive_along_simulation_MIP.append(simu_MIP.targets_alive_ts)
            self.scores_for_simulations_MIP.append(simu_MIP.score)
            self.time_to_kill_everybody_MIP.append(simu_MIP.time_to_kill_everybody)
            self.GBAD_health_MIP.append(simu_MIP.GBAD_health_state)
            self.damage_MIP.append(simu_MIP.theo_damage)
            self.nbd_drones_escaped_MIP.append(simu_MIP.nbd_drones_escaped)
            ####************************************#######
            ####************************************#######
            ####   ELEMENTS FOR THE DYNAMIC V1      #######
            Gun1_dynamic = Weapons.Gun('Gun1', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            Gun2_dynamic = Weapons.Gun('Gun2', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            grenade1_dynamic = Weapons.Grenade('Grenade1', 50, np.array([False, False]), self.weapons_desired['Grenade'][1])
            Laser1_dynamic = Weapons.Laser('Laser1', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            Laser2_dynamic = Weapons.Laser('Laser2', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            weapons_list2 = [Gun1_dynamic, Gun2_dynamic, grenade1_dynamic, Laser1_dynamic]
            random_swarm2 = Random(self.number_of_drones,60)
            print(f'Distance to base : {[np.linalg.norm(d.pos) for d in random_swarm2.drone_list]}')
            base2 = GBAD(np.array([0, 0, 0]), random_swarm2.drone_list, weapons_list2)
            ### Proceeding all the Dynamic simulations
            simu_Dynamic = Sim_dynamic(self.st, self.time_step, base2, [4, 2, 1, 1.75, 10])
            number_of_drones_destroyed_Dynamic = simu_Dynamic.simu_dynamic()[0]
            self.alive_along_simulation_Dynamic.append(simu_Dynamic.targets_alive_ts)
            self.score_for_simulation_Dynamic.append(simu_Dynamic.score)
            self.time_to_kill_everybody_Dynamic.append(simu_Dynamic.score)
            self.GBAD_health_Dynamic.append(simu_Dynamic.GBAD_health_state)
            self.damage_Dynamic.append(simu_Dynamic.theo_damage)
            print(f'damage_dynamic = {self.damage_Dynamic}')
            self.nbd_drones_escaped_Dynamic.append(simu_Dynamic.nbd_drones_escaped)
            ####************************************#######
            ####************************************#######
            ####   ELEMENTS FOR THE DYNAMIC V2      #######
            Gun1_dynamic_v2 = Weapons.Gun('Gun1', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            Gun2_dynamic_v2 = Weapons.Gun('Gun2', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            grenade1_dynamic_v2 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), self.weapons_desired['Grenade'][1])
            Laser1_dynamic_v2 = Weapons.Laser('Laser1', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            Laser2_dynamic_v2 = Weapons.Laser('Laser2', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            weapons_list2_v2 = [Gun1_dynamic_v2, Gun2_dynamic_v2, grenade1_dynamic_v2, Laser1_dynamic_v2]
            random_swarm2_v2 = Random(self.number_of_drones, 60)
            base3 = GBAD(np.array([0, 0, 0]), random_swarm2_v2.drone_list, weapons_list2_v2)
            print(f'Distance to base : {[np.linalg.norm(d.pos) for d in random_swarm2_v2.drone_list]}')
            ### Proceeding all the Dynamic simulations
            simu_Dynamic_v2 = Sim_dynamic(self.st, self.time_step, base3, [1, 1, 1, 1, 1])
            number_of_drones_destroyed_Dynamic = simu_Dynamic_v2.simu_dynamic()[0]
            self.alive_along_simulation_Dynamic_v2.append(simu_Dynamic_v2.targets_alive_ts)
            self.score_for_simulation_Dynamic_v2.append(simu_Dynamic_v2.score)
            self.GBAD_health_Dynamic_v2.append(simu_Dynamic_v2.GBAD_health_state)
            self.damage_Dynamic_v2.append(simu_Dynamic_v2.theo_damage)
            self.nbd_drones_escaped_Dynamic_v2.append(simu_Dynamic_v2.nbd_drones_escaped)
            ####************************************#######
            ####************************************#######
            ####   ELEMENTS FOR THE DYNAMIC V3      #######
            # Gun1_dynamic_v3 = Weapons.Gun('Gun1', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            # Gun2_dynamic_v3 = Weapons.Gun('Gun2', 50, np.array([False, False]), self.weapons_desired['Gun'][1])
            # grenade1_dynamic_v3 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), self.weapons_desired['Grenade'][1])
            # Laser1_dynamic_v3 = Weapons.Laser('Laser1', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            # Laser2_dynamic_v3 = Weapons.Laser('Laser2', 50, np.array([False, False]), self.weapons_desired['Laser'][1])
            # weapons_list2_v3 = [Gun1_dynamic_v3, Gun2_dynamic_v3, grenade1_dynamic_v3, Laser1_dynamic_v3]
            # random_swarm2_v3 = Random(self.number_of_drones, 60)
            # base4 = GBAD(np.array([0, 0, 0]), random_swarm2_v3.drone_list, weapons_list2_v3)
            # print(f'Distance to base : {[np.linalg.norm(d.pos) for d in random_swarm2_v3.drone_list]}')
            # ### Proceeding all the Dynamic simulations
            # simu_Dynamic_v4 = Sim_dynamic_v4(self.st, self.time_step, base4, [4, 2, 1, 1.75, 3])
            # number_of_drones_destroyed_Dynamic = simu_Dynamic_v4.simu_dynamic_v4()[0]
            # self.alive_along_simulation_Dynamic_v3.append(simu_Dynamic_v4.targets_alive_ts)
            # self.score_for_simulation_Dynamic_v3.append(simu_Dynamic_v4.score)
            # self.GBAD_health_Dynamic_v3.append(simu_Dynamic_v4.GBAD_health_state)
            # self.damage_Dynamic_v3.append(simu_Dynamic_v4.theo_damage)
            #
            # self.nbd_drones_escaped_Dynamic_v3.append(simu_Dynamic_v4.nbd_drones_escaped)


        return self.alive_along_simulation_MIP, self.alive_along_simulation_Dynamic


stats1 = Stats(100,80, 1, {'Gun': [2, 50], 'Grenade': [1, 30], 'Laser': [1, 25]}, 30)




time_for_simulation = np.arange(stats1.st)
time_for_plotting = stats1.statistic()
# print(f'Length of damage dynamic = {len(stats1.damage_Dynamic[0])}')
# print(f'Length of damage dynamic  v2 = {len(stats1.damage_Dynamic_v2[0])}')
# # print(f'Length of damage dynamic  v3 = {len(stats1.damage_Dynamic_v3[0])}')
# print(f'Number of targets alive {stats1.alive_along_simulation_Dynamic}')

def average_results(results_MIP):
    new_lists = [[] for _ in range(len(results_MIP[0]))]
    # Parcourir chaque sous-liste et ajouter les éléments aux nouvelles listes
    for sublist in results_MIP:
        for i, elem in enumerate(sublist):
            new_lists[i].append(elem)
    avg_list = []
    # Afficher les nouvelles listes
    for lst in new_lists:
        avg_list.append(statistics.mean(lst))
    return avg_list


#### Getting the results for the NUMBER OF DRONES DESTROYED ####
results_nbd_MIP = stats1.alive_along_simulation_MIP
results_nbd_Dynamic = stats1.alive_along_simulation_Dynamic
results_nbd_Dynamic_v2 = stats1.alive_along_simulation_Dynamic_v2
# results_nbd_Dynamic_v3 = stats1.alive_along_simulation_Dynamic_v3

#### Get the average number of drones destroyed for both results MIP and Dynamic ####
avg_nbd_destroyed_MIP = average_results(results_nbd_MIP)
avg_nbd_destroyed_Dynamic_v1 = average_results(results_nbd_Dynamic)
avg_nbd_destroyed_Dynamic_v2 = average_results(results_nbd_Dynamic_v2)
# avg_nbd_destroyed_Dynamic_v3 = average_results(results_nbd_Dynamic_v3)

### Getting the results for the SCORE ###
results_score_MIP = stats1.scores_for_simulations_MIP
results_score_Dynamic = stats1.score_for_simulation_Dynamic
results_score_Dynamic_v2 = stats1.score_for_simulation_Dynamic_v2
# results_score_Dynamic_v3 = stats1.score_for_simulation_Dynamic_v3
print(f'Score MIP : {results_score_MIP}')
### Getting the results for the GBAD HEALTH ###
results_GBAD_health_MIP = stats1.GBAD_health_MIP
results_GBAD_health_Dynamic = stats1.GBAD_health_Dynamic
results_GBAD_health_Dynamic_v2 = stats1.GBAD_health_Dynamic_v2
# results_GBAD_health_Dynamic_v3 = stats1.GBAD_health_Dynamic_v3
### Getting the average for GBAD health.
avg_GBAD_health_MIP = average_results(results_GBAD_health_MIP)
avg_GBAD_health_Dynamic_v1 = average_results(results_GBAD_health_Dynamic)
avg_GBAD_health_Dynamic_v2 = average_results(results_GBAD_health_Dynamic_v2)
# avg_GBAD_health_Dynamic_v3 = average_results(results_GBAD_health_Dynamic_v3)

#### Getting the results for the THEORETICAL DAMAGE ####
results_damage_MIP = stats1.damage_MIP
results_damage_Dynamic = stats1.damage_Dynamic
results_damage_Dynamic_v2 = stats1.damage_Dynamic_v2
# results_damage_Dynamic_v3 = stats1.damage_Dynamic_v3
### Get the average of theoretical damage for MIP and Dynamic
#### Get the average number of drones destroyed for both results MIP and Dynamic
avg_damage_list_MIP = average_results(results_damage_MIP)
avg_damage_list_Dynamic = average_results(results_damage_Dynamic)
avg_damage_list_Dynamic_v2 = average_results(results_damage_Dynamic_v2)
# avg_damage_list_Dynamic_v3 = average_results(results_damage_Dynamic_v3)


#### Getting the results for the NUMBER OF DRONES ESCAPED ####
results_nbd_drones_escaped_MIP = stats1.nbd_drones_escaped_MIP
results_nbd_drones_escaped_Dynamic = stats1.nbd_drones_escaped_Dynamic
results_nbd_drones_escaped_Dynamic_v2 = stats1.nbd_drones_escaped_Dynamic_v2
# results_nbd_drones_escaped_Dynamic_v3 = stats1.nbd_drones_escaped_Dynamic_v3
print(f'Number of drones escape Dynamic : {results_nbd_drones_escaped_Dynamic}')
#### Get the average number of drones escaped
avg_nbd_drones_escaped_MIP = average_results(results_nbd_drones_escaped_MIP)
avg_nbd_drones_escaped_Dynamic = average_results(results_nbd_drones_escaped_Dynamic)
avg_nbd_drones_escaped_Dynamic_v2 = average_results(results_nbd_drones_escaped_Dynamic_v2)
# avg_nbd_drones_escaped_Dynamic_v3 = average_results(results_nbd_drones_escaped_Dynamic_v3)




### Plotting data
simulation_number = [k+1 for k in range(0,30)]
fig, axs = plt.subplots(nrows=5,ncols=4, figsize=(15,7))
fig.suptitle(f'{stats1.number_of_drones} Drones, 4 Weapons, Simul time = {stats1.st}, init_pos = [30, 35]')
for k in range (len(results_nbd_Dynamic)):
    axs[0][0].plot(time_for_simulation, results_nbd_MIP[k], linewidth ='1', linestyle='--')
    axs[0][0].set_title('MIP')
    # axs[0][3].plot(time_for_simulation, results_nbd_Dynamic_v3[k], linewidth ='1', linestyle='--' )
    axs[0][3].set_title('Vf1(), Lambda= 5exp(x/x-1)')
    axs[0][3].set_xlabel('Time in s')
    axs[0][3].set_ylabel('Number of drones alive')
    axs[0][1].sharey(axs[0][0])
    axs[3][0].plot(time_for_simulation, results_nbd_drones_escaped_MIP[k], linewidth='1', linestyle='--')
    axs[3][0].set_xlabel('Time in s')
    axs[3][0].set_ylabel('Drones escape')
    axs[3][1].plot(time_for_simulation, results_nbd_drones_escaped_Dynamic[k],linewidth='1', linestyle='--' )
    axs[3][1].set_xlabel('Time in s')
    axs[3][1].set_ylabel('Drones escape')
    axs[3][2].plot(time_for_simulation, results_nbd_drones_escaped_Dynamic_v2[k], linewidth='1', linestyle='--')
    axs[3][2].set_xlabel('Time in s')
    axs[3][2].set_ylabel('Drones escape')
    # axs[3][3].plot(time_for_simulation, results_nbd_drones_escaped_Dynamic_v3[k], linewidth='1', linestyle='--')
    axs[3][3].set_xlabel('Time in s')
    axs[3][3].set_ylabel('Drones escape')


    # axs[1][3].plot(time_for_simulation, results_damage_Dynamic_v3[k], linewidth ='1', linestyle='--')
    axs[1][3].set_xlabel('Time in s')
    axs[1][3].set_ylabel('Damage capability')
    axs[4][0].plot(simulation_number, results_score_MIP, linewidth='2', linestyle='-')
    axs[4][0].set_xlabel('Simulation number')
    axs[4][0].set_ylabel('Score')
    # axs[4][3].plot(simulation_number, results_score_Dynamic_v3, linewidth='2', linestyle='-')
    axs[4][3].set_xlabel('Score')
    axs[4][3].set_ylabel('Simulation number ')

    # axs[2][3].plot(time_for_simulation, results_GBAD_health_Dynamic_v3[k], linewidth ='1', linestyle='--')
    axs[2][3].set_xlabel('Time in s')
    axs[2][3].set_ylabel('GBAD Health')
    axs[2][0].plot(time_for_simulation,results_GBAD_health_MIP[k], linewidth='1', linestyle='--')
    axs[2][0].set_xlabel('Time in s')
    axs[2][0].set_ylabel('GBAD Health')
    axs[2][0].set_ylim(0.30, 1.02)
    axs[1][0].plot(time_for_simulation, results_damage_MIP[k], linewidth='1', linestyle='--')
    axs[1][0].set_xlabel('Time in s')
    axs[1][0].set_ylabel('Damage capability')
    axe1 = axs[1][0]    ## to keep the same scale between the 2 subplots of the score
    axe3 = axs[2][0]
    axe4 = axs[2][1]
    axe5 = axs[2][2]
    axey_damage_capability = axs[3][0]
    axey_damage_capability_dynamic_v1 = axs[3][1]
    axey_damage_capability_dynamic_v2 = axs[3][2]
    axey_damage_capability.sharey(axey_damage_capability_dynamic_v1)
    axey_damage_capability_dynamic_v2.sharey(axey_damage_capability)
    axs[0][1].plot(time_for_simulation, results_nbd_Dynamic[k],  linewidth='1', linestyle='--')
    axs[0][1].set_title('Vf1(), [4, 2, 1, 1.75, 10]')
    # axs[1][1].plot(time_for_simulation, results_score_Dynamic[k], linewidth='1', linestyle='--')
    axs[4][1].plot(simulation_number, results_score_Dynamic, linewidth='2', linestyle='-')
    axs[2][1].plot(time_for_simulation, results_GBAD_health_Dynamic[k], linewidth='1', linestyle='--')
    axs[1][1].plot(time_for_simulation, results_damage_Dynamic[k], linewidth='1', linestyle='--')
    axs[1][1].set_xlabel('Time in s')
    axs[1][1].set_ylabel('Damage capability')
    axs[2][1].set_xlabel('Time in s')
    axs[2][1].set_ylabel('GBAD Health')
    axs[1][1].set_xlabel('Time in s ')
    axs[4][1].set_ylabel('Score')
    axs[4][1].set_xlabel('Simulation number ')
    axe2 = axs[1][1]

    axs[0][2].plot(time_for_simulation, results_nbd_Dynamic_v2[k], linewidth='1', linestyle='--')
    axs[0][2].set_title('Vf2(), [1, 1, 1, 1, 1]')
    axs[4][2].plot(simulation_number, results_score_Dynamic_v2, linewidth ='2', linestyle='-')
    axs[2][2].plot(time_for_simulation, results_GBAD_health_Dynamic_v2[k], linewidth ='1', linestyle='--')
    axs[1][2].plot(time_for_simulation, results_damage_Dynamic_v2[k], linewidth ='1', linestyle ='--')
    axs[1][2].set_xlabel('Time in s')
    axs[1][2].set_ylabel('Damage capability')
    axs[2][2].set_xlabel('Time in s')
    axs[2][2].set_ylabel('GBAD Health')
    axs[4][2].set_xlabel('Simulation')
    axs[4][2].set_ylabel('Score')

fig.subplots_adjust(wspace = 0.5, hspace = 0.5 )
axs[0][0].plot(time_for_simulation, avg_nbd_destroyed_MIP, linewidth='3', linestyle='-', color='black')
axs[0][2].plot(time_for_simulation, avg_nbd_destroyed_Dynamic_v2, linewidth='3', linestyle ='-', color='black')
# axs[0][3].plot(time_for_simulation, avg_nbd_destroyed_Dynamic_v3, linewidth='3', linestyle ='-', color='black')
axs[1][0].plot(time_for_simulation, avg_damage_list_MIP, linewidth='3', linestyle='-', color='black')
# axs[1][3].plot(time_for_simulation, avg_damage_list_Dynamic_v3, linewidth='3', linestyle='-', color='black')
# axs[2][3].plot(time_for_simulation, avg_GBAD_health_Dynamic_v3, linewidth='3', linestyle='-', color='black')


axs[0][1].plot(time_for_simulation, avg_nbd_destroyed_Dynamic_v1, linewidth='3', linestyle='-', color='black')

axs[1][1].plot(time_for_simulation, avg_damage_list_Dynamic, linewidth='3', linestyle='-', color='black')
axs[1][2].plot(time_for_simulation, avg_damage_list_Dynamic_v2, linewidth ='3', linestyle='-', color='black')

axs[2][0].plot(time_for_simulation, avg_GBAD_health_MIP, linewidth='3', linestyle='-', color='black')
# axs[2][0].axhline(y=get_asymp(avg_GBAD_health_MIP, time_for_simulation), color ='g', linestyle='dashdot')
axs[2][1].plot(time_for_simulation, avg_GBAD_health_Dynamic_v1, linewidth='3', linestyle='-', color='black')
axs[2][2].plot(time_for_simulation, avg_GBAD_health_Dynamic_v2, linewidth='3', linestyle='-', color='black')


axs[3][0].plot(time_for_simulation, avg_nbd_drones_escaped_MIP, linewidth='3', linestyle='-', color='black')
axs[3][1].plot(time_for_simulation, avg_nbd_drones_escaped_Dynamic, linewidth='3', linestyle='-', color='black')
axs[3][2].plot(time_for_simulation, avg_nbd_drones_escaped_Dynamic_v2, linewidth='3', linestyle='-', color='black' )
# axs[3][3].plot(time_for_simulation, avg_nbd_drones_escaped_Dynamic_v3, linewidth='3', linestyle='-', color='black')
axs[0][0].set_xlabel('Time in s')
axs[0][1].set_xlabel('Time in s')
axs[0][0].set_ylabel('Number of drones alive')
axs[0][1].set_ylabel('Number of drones alive')
axs[0][2].set_ylabel('Number of drones alive')
axs[0][2].set_xlabel('Time in s')
axs[0][0].sharey(axs[0][1])
axs[0][2].sharey(axs[0][1])
axs[0][3].sharey(axs[0][2])

axs[1][1].sharey(axs[1][0])
axs[1][2].sharey(axs[1][1])
axs[1][3].sharey(axs[1][2])

axs[2][1].sharey(axs[2][0])
axs[2][2].sharey(axs[2][1])
axs[2][3].sharey(axs[2][2])


plt.show()





