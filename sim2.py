import Drone as Drones
from Linear_Assignment import Linear_Assignment
from MIP_Assignment import MIP_Assignment
import gbad
import Weapons
import numpy as np
import pandas as pd

class Sim2:

    def __init__(self, st, time_step, base):
        self.st = st # End time in simulation
        self.nbd = len(base.drone_list) # Number of drones
        self.time_step = time_step
        self.drone_list = base.drone_list
        self.base = base
        self.n = len(base.weapons)
        self.assignment = None
        self.downtime_timer = 0
        self.count_alive = []
        self.the_time_steps = []

    def next(self):                                                    ## This function proceed to the global simulation 
        w_prob = [w.Pc for w in self.base.weapons]
        # Create cost/probability matrix
        for t in range (0,self.st, self.time_step) :                        ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f'Downtime Timer = {self.downtime_timer}')
            self.base.get_closest_drones(self.n)
            cost = np.reshape(np.repeat(w_prob, self.n), (self.base.nw, self.n))
            dist = self.base.get_closest_drones(self.n)  # Get closest drones
            print(f'the closest drones are at the distance {dist}')
            for index, w in enumerate(self.base.weapons):
                cost[index] = cost[index] * [d < w.rc for d in dist]
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)
                if np.mod(self.downtime_timer, w.downtime) != 0 :    # means that weapon is not  available
                    print(f' {w.name} is not available')
                    cost[index] = [0]*len(self.base.get_closest_drones(self.n))
            print(cost)
            self.assignment = MIP_Assignment(cost, self.base.weapons, self.base.closest_drones)
            for i in self.assignment.assignement:
                self.base.closest_drones[i[1]].drone_get_destroyed(self.base.weapons[i[0]])     #
            for k in self.drone_list:
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step
            counter_active = 0
            for alive in self.drone_list :
                if alive.active == 1:
                    counter_active += 1        # number of UAVs live at time step
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t)
        return self.the_time_steps, self.count_alive


###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####


## Get the weapons ###
Gun1 = Weapons.Gun('Gun1',50,np.array([False, False]))
Gun2 = Weapons.Gun('Gun2',50,np.array([False, False]))
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]))
Laser1 = Weapons.Laser('Laser1',50, np.array([False, False]))
Laser2 = Weapons.Laser('Laser2',50, np.array([False, False]))


n = 4                 # number of weapons #
initial_swarm = Drones.Ball(25, 5, np.array([50,30, 40]), 0.58)
base = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])

simul = Sim2(5, 1, base)
final_nb_drones_alive = simul.next()[1][-1]
print(f'The final number of UAVs alive is : {final_nb_drones_alive}')

