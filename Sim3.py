import Drone as Drones
from Linear_Assignment import Linear_Assignment
from MIP_Assignment import MIP_Assignment
import GBAD
import Weapons
import numpy as np
from math import *
from Jonk_Volg import Jonk_Volg

class Sim3:

    def __init__(self, st, time_step, base):
        self.st = st # End time in simulation
        self.nbd = len(base.drone_list) # Number of drones
        self.time_step = time_step
        self.drone_list = base.drone_list
        self.base = base
        self.n = len(self.drone_list)
        self.assignment = None
        self.downtime_timer = 0
        self.count_alive = [len(base.drone_list)]
        self.the_time_steps = [0]

    def next3(self):
        w_prob = [w.Pc for w in self.base.weapons]
        # Create cost/probability matrix
        for t in np.arange (0,self.st, self.time_step) :                        ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f'Downtime Timer = {self.downtime_timer}')
            cost = np.reshape(np.repeat(w_prob, self.n), (self.base.nw, self.n))
            print(cost)
            dist = self.base.get_distance_drone()
            for index, w in enumerate(self.base.weapons):
                cost[index] = cost[index] * [d < w.rc for d in dist]
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)
                if np.mod(self.downtime_timer, w.downtime) != 0 :    # means that weapon is not  available
                    print(f' {w.name} is not available')
                    cost[index] = [0]*self.n
            print(cost)
            self.assignment = Jonk_Volg(cost, self.base.weapons, self.base.drone_list)
            for i in self.assignment.assignement:
                self.base.drone_list[i[1]].drone_get_destroyed(self.base.weapons[i[0]])     #
            for k in self.drone_list:
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step
            counter_active = 0
            for alive in self.drone_list :
                if alive.active == 1:
                    counter_active += 1        # number of UAVs live at time step
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t+1)
        s=0
        for a in self.drone_list :
            if a.active == 1 :
                s += 1
        print(f'There is still {s} UAV alive in the swarm')
        return self.the_time_steps, self.count_alive



n = 30  # number of weapons #

### Get the weapons for the fisrt base ###
Gun1 = Weapons.Gun(0,np.array([False, False]))
Gun2 = Weapons.Gun(0,np.array([False, False]))
Gun3 = Weapons.Gun(0,np.array([False, False]))
Gun4 = Weapons.Gun(0,np.array([False, False]))
grenade1 = Weapons.Grenade(0, np.array([False, False]))
grenade2 = Weapons.Grenade(0, np.array([False, False]))
Laser1 = Weapons.Laser(0, np.array([False, False]))
Laser2 = Weapons.Laser(0, np.array([False, False]))
Laser3 = Weapons.Laser(0, np.array([False, False]))
Laser4 = Weapons.Laser(0, np.array([False, False]))


initial_swarm = Drones.Ball(15, 5, np.array([5, 5, 4]), 0.58)
base = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, Gun3, Gun4, grenade1, grenade2,
                                                                     Laser1, Laser2, Laser3, Laser4])


### Get the weapons for the second base ###
Gun5 = Weapons.Gun(0,np.array([False, False]))
Gun6 = Weapons.Gun(0,np.array([False, False]))
Gun7 = Weapons.Gun(0,np.array([False, False]))
Gun8 = Weapons.Gun(0,np.array([False, False]))
grenade3 = Weapons.Grenade(0, np.array([False, False]))
grenade4 = Weapons.Grenade(0, np.array([False, False]))
Laser5 = Weapons.Laser(0, np.array([False, False]))
Laser6 = Weapons.Laser(0, np.array([False, False]))
Laser7 = Weapons.Laser(0, np.array([False, False]))
Laser8 = Weapons.Laser(0, np.array([False, False]))

initial_swarm2 = Drones.Ball(15, 5, np.array([5, 5, 4]), 0.58)
base2 = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm2.drone_list, [Gun5, Gun6, Gun7, Gun8, grenade3, grenade4,
                                                                     Laser5, Laser6, Laser7, Laser8])
simulation = Sim3(5, 1, base)
simulation.next3()

# [(0, 0), (3, 8), (4, 9), (5, 1), (6, 2), (7, 3), (9, 4), (8, 5), (1, 7), (2, 6)]
# total_cost = 0
# for k in range (len(a)) :
#     total_cost += cost[a[k][0]][a[k][1]]
# print(total_cost)
#
# total_cost = 0
# for aa in a:
#     total_cost += cost[aa[0],aa[1]]