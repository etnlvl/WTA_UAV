from Drone import Ball

import Weapons
import numpy as np
from gbad import GBAD
from policy_assignment import Policy

class Sim_Almost_MDP :
    def __init__(self, st, time_step, base):
        self.st = st  # End time in simulation
        self.nbd = len(base.drone_list)  # Number of drones
        self.time_step = time_step
        self.drone_list = base.drone_list
        self.base = base
        self.n = len(base.weapons)
        self.assignment = None
        self.downtime_timer = 0
        self.count_alive = []
        self.the_time_steps = []


    def sim_almost_mdp(self, assignment):
        for time in range(self.st):
            for weapon_idx, weapon_assignment in assignment.items():
                print(weapon_idx, weapon_assignment)
                print(f'Weapon assignment size is {len(weapon_assignment)}')
                # print(weapon_assignment[time])
                self.base.drone_list[weapon_assignment[time].idx].drone_get_destroyed(self.base.weapons[int(weapon_idx)])
            for k in self.drone_list:
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            counter_active = 0
            for alive in self.drone_list:
                if alive.active == 1:
                    counter_active += 1     ## number of drones alive at time step
            self.count_alive.append(counter_active)
        return self.count_alive[-1]

### Create the weapons ###
Gun1 = Weapons.Gun('Gun1',50,np.array([False, False]))
Gun2 = Weapons.Gun('Gun2',50,np.array([False, False]))
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]))
Laser1 = Weapons.Laser('Laser1',50, np.array([False, False]))
Laser2 = Weapons.Laser('Laser2',50, np.array([False, False]))

### Create the base ###
initial_swarm = Ball(30, 5, np.array([50,30, 40]), 0.58)
base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2,
                                                                     grenade1, Laser1])

simulation = Sim_Almost_MDP(20,1, base)

### Create the global policy ###
first_policy = Policy(0, len(base.drone_list), 5)
policy = first_policy.get_first_policy(base.get_closest_drones(first_policy.n_assignments)[1])

print('this is the first policy')
print(policy)


first_policy.initialize_surv_prob(policy, [Gun1.Pc, Gun2.Pc, grenade1.Pc, Laser1.Pc])
assign = first_policy.get_all_policies(simulation.n,[Gun1.Pc, Gun2.Pc, grenade1.Pc, Laser1.Pc], base.drone_list)

battle = simulation.sim_almost_mdp(assign)
print(f'There is still {battle} drones alive at the end of the simulation')





