from Drone import Ball

import Weapons
import numpy as np
from gbad import GBAD
from policy_assignment import Policy
from Drone import Drone

class Sim_nth_timestep:
    def __init__(self, st, time_step):
        self.st = st  # End time in simulation
        self.time_step = time_step
        self.assignment = None
        self.downtime_timer = 0
        self.count_alive = []
        self.the_time_steps = []
        self.score = 0


    def simulator(self, time_period):
        ### Create the weapons ###
        gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
        gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
        grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
        laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
        laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 9)
        ### Create the base ###
        initial_swarm = Ball(30
                             , 5, np.array([30, 20, 15]), 2)
        print(f'initial swarm {initial_swarm.drone_list}')
        base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [gun1, gun2,
                                                                    grenade1, laser1])
        random_time_spone = 10         ### we decide that at this time, one drone more dangerous will spone in the simulation
        print(f'the random spone is {random_time_spone}')
        for time in range(self.st):
            print(f'time step = {time}')
            threat_values = [drone.update_TV() for drone in base.drone_list]
            if time == random_time_spone:                                                            ### create a heavy payload dangerous drone at a random time during the simulation
                print('The drone with a heavy payload will enter into the simulation')
                tv_max = max(threat_values)                                                          ### picking the highest threat value among all the drones.
                drone = Policy.find_drone_tv(Policy, tv_max, base.drone_list)                        ### finding the drone with the highest threat value corresponding.
                print(drone)
                new_pos = drone.pos + np.array([drone.pos[0]+5, drone.pos[1]+2, drone.pos[2]+12])                                     ### creating a drone with a heavy payload (threat value bigger than the highest found just above) and making it appears
                                                                                                     ### just next to it.
                dangerous_drone = Drone(new_pos, len(base.drone_list),None)                ### creating the corresponding object.
                dangerous_drone.threat_val = tv_max + 10                                             ### setting the corresponding threat value.
                base.drone_list.append(dangerous_drone)                                              ### Adding it to the drone list.
                print(f'The most dangerous drone {dangerous_drone.idx} just appears and its threat value is equal to {dangerous_drone.threat_val}')

            drones_alive = base.get_all_live_drones()
            closest_drones = base.get_closest_drones(time_period)[1]
            highest_TV_drones = base.get_highest_TV_drones(time_period)[1]
            print(f'the list of the highest threat_value drone is :{[drone_index.idx for drone_index in highest_TV_drones]} and there is {len(highest_TV_drones)} of them')
            # print(f'Length of closest drones is actually : {len(closest_drones)}')
            if time % time_period == 0:                      ### we build a new policy every time_period-th time step
                policy = Policy([gun1, gun2, grenade1, laser1], len(base.drone_list), time_period)
                first_policy = policy.get_first_policy(highest_TV_drones)

                if policy == None:
                    break
                policy.initialize_surv_prob(first_policy, [gun1.Pc, gun2.Pc, grenade1.Pc, laser1.Pc])
                assign = policy.get_all_policies(drones_alive, base.drone_list)
                assignment_readable = dict()
                for key, value in assign.items():
                    assignment_readable[key] = [d.idx for d in value]
                print(f'the assignment for the next {time_period} time step is {assignment_readable}')
                # print(f'Length of alive_drones_list : {len(drones_alive)}')
            for weapon_idx, weapon_assignment in assign.items():
                # print(f'The weapons of the base are {base.weapons}')
                # print(f'weapon_idx is sthg like this {type(weapon_idx)}')
                weapon_to_use = Weapons.Weapons.find_weapon(Weapons, weapon_idx, base.weapons)
                # print(f'The Weapon to use is {weapon_to_use}')
                base.drone_list[weapon_assignment[time % time_period].idx].drone_get_destroyed(weapon_to_use)
                if base.drone_list[weapon_assignment[time % time_period].idx].active == 0:
                    self.score += base.drone_list[weapon_assignment[time % time_period].idx].threat_val
                    print(f'the added value to the score is : {base.drone_list[weapon_assignment[time % time_period].idx].threat_val}')

            for k in base.drone_list:
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            counter_active = 0
            for alive in base.drone_list:
                if alive.active == 1:
                    counter_active += 1
            self.count_alive.append(counter_active)
        return self.count_alive[-1]

simulation = Sim_nth_timestep(20, 1)
battle = simulation.simulator(5)
print(f'There is still {battle} drones alive at the end of the simulation')
print(f'Final score = {simulation.score}')




