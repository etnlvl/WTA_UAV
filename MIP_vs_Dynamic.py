from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
from Drone import Line
import matplotlib.pyplot as plt
import Weapons
import numpy as np
from Drone import Drone
import statistics
from Value_function import Feed_MIP
from Sim_dynamic import Sim_dynamic
from MIP_for_comparaison import Sim2


target_alive_greedy = []
gbad_greedy = []
damage_cap_greedy = []
score_of_simu_greedy = []

target_alive_dynamic = []
gbad_dynamic = []
damage_cap_dynamic = []
score_of_simu_dynamic = []
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



fig, axs = plt.subplots(2,1, figsize=(9, 7))

for k in range(nb_simulations) :
    Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
    Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
    grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
    Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
    Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
    swarm = Random(100, 60)
    base = GBAD(np.array([0, 0, 0]), swarm.drone_list, [Gun1, Gun2, grenade1,
                                                               Laser1])
    simu = Sim2(60, 1, base)
    simu.next()


    Gun12 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
    Gun22 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
    grenade12 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
    Laser12 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
    Laser22 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)
    swarm2 = Random(100, 60)
    base2 = GBAD(np.array([0, 0, 0]), swarm2.drone_list, [Gun12, Gun22, grenade12,
                                                        Laser12])
    simu2 = Sim_dynamic(60, 1, base2, [1, 1, 1, 1, 1])
    simu2.simu_dynamic()
    target_alive_dynamic.append(simu2.targets_alive_ts)
    gbad_dynamic.append(simu2.GBAD_health_state)
    damage_cap_dynamic.append(simu2.theo_damage)
    score_of_simu_dynamic.append(simu2.score)
    print(f'targets alive : {simu.targets_alive_ts}')
    # axs[0].plot(simu.GBAD_health_state, linewidth='1', linestyle ='--')
    # axs[0].set_xlabel('Time in s')
    # axs[0].set_ylabel('GBAD health')

    # axs[1].plot(simu.theo_damage, linewidth='1', linestyle ='--')
    # axs[1].set_xlabel('Time in s')
    # axs[1].set_ylabel('Damage capability')
    target_alive_greedy.append(simu.targets_alive_ts)
    gbad_greedy.append(simu.GBAD_health_state)
    damage_cap_greedy.append(simu.theo_damage)
    score_of_simu_greedy.append(simu.score)

average_targets_alive_greedy = average_results(target_alive_greedy)
average_health_greedy = average_results(gbad_greedy)
average_damage_greedy = average_results(damage_cap_greedy)
average_targets_alive_dynamic = average_results(target_alive_dynamic)
average_health_dynamic = average_results(gbad_dynamic)
average_damage_dynamic = average_results(damage_cap_dynamic)

axs[0].plot(average_targets_alive_greedy, linewidth ='3', linestyle= '-', color='r', label='greedy')
axs[0].plot(average_targets_alive_dynamic, linewidth ='3', linestyle= '-', color='b', label='dynamic')
axs[0].set_ylabel('Number of drones alive')
axs[0].set_xlabel('Time in s')
axs[0].legend(loc='upper right')


axs[1].plot(average_health_greedy, linewidth='3', linestyle='-', color='r', label='greedy')
axs[1].plot(average_health_dynamic, linewidth='3', linestyle='-', color='b', label='dynamic')
axs[1].set_ylabel('GBAD health')
axs[1].set_xlabel('Time in s')

plt.show()