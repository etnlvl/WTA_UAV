from Drone import Ball

import Weapons
import numpy as np
from gbad import GBAD
from transit import Policy

class Sim_nth_timestep:
    def __init__(self, st, time_step):
        self.st = st  # End time in simulation
        self.time_step = time_step
        self.assignment = None
        self.downtime_timer = 0
        self.count_alive = []
        self.the_time_steps = []


    def simulator(self, time_period):
        ### Create the weapons ###
        gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]))
        gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]))
        grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]))
        laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]))
        laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]))
        ### Create the base ###
        initial_swarm = Ball(30, 5, np.array([50, 30, 40]), 0.58)
        base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [gun1, gun2,
                                                                    laser1, laser2])
        for time in range(self.st):
            print(f'time step = {time}')
            drones_alive = base.get_all_live_drones()
            closest_drones = base.get_closest_drones(time_period)
            if time % time_period == 0:                      ### we build a new policy every time_period-th time step
                first_policy = Policy(0, len(base.drone_list), time_period)
                policy = first_policy.get_first_policy(closest_drones)
                first_policy.initialize_surv_prob(policy, [gun1.Pc, gun2.Pc, grenade1.Pc, laser1.Pc])
                assign = first_policy.get_all_policies(len(base.weapons), [gun1.Pc, gun2.Pc, grenade1.Pc, laser1.Pc], base.drone_list)
                print(f'the assignment for the next {time_period} time step is {assign}')
                print(f'Length of alive_drones_list : {len(drones_alive)}')
            for weapon_idx, weapon_assignment in assign.items():
                base.drone_list[weapon_assignment[time % time_period].idx].drone_get_destroyed(base.weapons[int(weapon_idx)])
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




