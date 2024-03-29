import Drone as Drones
from Linear_Assignment import Linear_Assignment
from MIP_Assignment import MIP_Assignment
import gbad
import Weapons
import numpy as np
from math import *
import pandas as pd

class Sim_MDP:

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

    def next_MDP(self):
        w_prob = [w.Pc for w in self.base.weapons]
        print(self.drone_list[3])
        for t in np.arange (0,self.st, self.time_step) :                        ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f'Downtime Timer = {self.downtime_timer}')
            dist = self.base.get_distance_drone()
            print(dist)
            cost = np.reshape(np.repeat(w_prob, self.n), (self.base.nw, self.n))
            for index, w in enumerate(self.base.weapons):
                cost[index] = cost[index] * [w.range_window[0] <= d <= w.range_window[1] for d in dist]
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)
                cost[index] = [w.reward_value * element for element in cost[index]]

                if np.mod(self.downtime_timer, w.downtime) != 0 :    # means that weapon is not  available
                    # print(f' {w.name} is not available')
                    cost[index] = [0]*self.n
            print(cost)
            self.assignment = MIP_Assignment(cost, self.base.weapons, self.base.drone_list)
            print(self.assignment)
            indexes_alloc_targets = [tup[1] for tup in self.assignment.assignement]
            indexes_alloc_weapons = [tup[0] for tup in self.assignment.assignement]
            ### First allocation is made, we have to check the environment's state  to build the next state ###
            ## Checking if the drone has been allocated and updating the corresponding weapon status ###
            for id, w in enumerate(self.base.weapons) :
                if id in indexes_alloc_weapons :
                    w.state_dependency[0] = True
                    self.drone_list[id].drone_allocated.append(w.name)

            ## Checking if the drone has been effectively destroyed and updating the status (through the function drone_get_destroyed)  ##
            for i in self.assignment.assignement:
                if self.base.drone_list[i[1]].drone_get_destroyed(self.base.weapons[i[0]]) :
                    self.base.weapons[i[0]].state_dependency[1] = True
                    self.base.weapons[i[0]].reward_value += 1
                else :
                    self.base.weapons[i[0]].reward_value += -1       ### give to weapon a negative reward if the drone is miss ###
                    print(f'{self.base.weapons[i[0]].name} receive a negative reward' )
            for drone in self.base.drone_list:                             ### give a heavier negative reward if one drone escapes from one weapon window_range ###
                for weapons in self.base.weapons :
                    if drone.drone_escape(weapons) and drone.active == 1 :
                        weapons.reward_value += -3
                        print(f'{weapons.name} receive a HEAVY negative reward'  )

            for agent in self.base.weapons :
                print(f'REWARD VALUE OF {agent.name}={agent.reward_value}')
            for k in self.drone_list:                  ###UPDATE THE DRONE'S POSITION IF STILL ALIVE
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step
            counter_active = 0
            for alive in self.drone_list :    ### COUNT THE NUMBER OF TARGETS ALIVE AT THE END OF THE SIMULATION ###
                if alive.active == 1:
                    counter_active += 1
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t+1)
        return self.the_time_steps, self.count_alive



n = 4  # number of weapons #

### Get the weapons for the fisrt base ###
Gun1 = Weapons.Gun('Gun1',50,np.array([False, False]))
Gun2 = Weapons.Gun('Gun2',50,np.array([False, False]))
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]))
Laser1 = Weapons.Laser('Laser1',50, np.array([False, False]))
Laser2 = Weapons.Laser('Laser2',50, np.array([False, False]))




initial_swarm = Drones.Ball(25, 5, np.array([50,30, 40]), 0.58)
base = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])
simulation = Sim_MDP(5, 1, base)
final_nb_drones_alive = simulation.next_MDP()[1][-1]
print(f'The final number of UAVs alive is : {final_nb_drones_alive}')

total_number_of_drones_alive = []
total_number_of_drones_alive.append(final_nb_drones_alive)
