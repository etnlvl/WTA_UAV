from Drone import Ball
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np
from Drone import Random


class Sim2:

    def __init__(self, st, time_step, base):
        self.st = st                            # End time in simulation
        self.nbd = len(base.drone_list)         # Number of drones
        self.time_step = time_step              # period of time for the assignment
        self.drone_list = base.drone_list       # take from GBAD the drone list, it contains, position, index..
        self.base = base
        self.n = len(base.weapons)              # number of weapons
        self.assignment = None                  # initialize the assignment at nothing at the beginning of the simulation
        self.downtime_timer = 0                 # Counter in order to measure if weapon is available regarding its downtime
        self.count_alive = []                   # list which retains the number of drones alive at each time step.
        self.the_time_steps = []
        self.targets_alive_ts = []
        self.GBAD_health_state = []
        self.theo_damage = []
        self.score = 0
        self.counter_drones_destroyed = 0
        self.time_to_kill_everybody = st


    "Sim2 and its function Sim2.next() makes run the battle by allocating weapons to targets with the MIP algorithm taken from the library OR tools"

    def next(self):                                                                                 ## This function proceed to the global simulation
        w_prob = [w.Pc for w in self.base.weapons]
                                                                                                    ## Create cost/probability matrix
        for t in range (0,self.st, self.time_step):                                                 ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            self.the_time_steps.append(t)
            self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
            self.GBAD_health_state.append(self.base.health)
            print(f'Downtime Timer = {self.downtime_timer}')
            closest_drones = []
            print(f'{self.base.get_closest_drones(self.n)[1]}')
            cost = np.reshape(np.repeat(w_prob, len(self.base.closest_drones)), (self.base.nw, -1))
            dist = [np.linalg.norm(element.pos - np.array([0, 0, 0])) for element in self.base.closest_drones]                                         ## gets all n-weapons the closest drones to assign it later with the MIP algorithm
            print(f'the closest drones are at the distance {dist}')
            if len(dist) == 0:
                self.time_to_kill_everybody = t
                break
            for index, w in enumerate(self.base.weapons):
                print(f'cost[index] ={cost[index]}')
                cost[index] = cost[index] * [w.range_window[0] <= d <= w.range_window[1] for d in dist]                                ## set a zero probability in the cost matrix if the drone is out of range of the weapon
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], len(self.base.closest_drones))                                                   ## set a zero probability in the cost matrix if corresponding weapon has no more ammunitions
                if np.mod(self.downtime_timer, w.downtime) != 0:                                                                       ## check if  weapon is ready and re-loading.
                    print(f' {w.name} is not available')
                    cost[index] = [0]*len(self.base.get_closest_drones(self.n))
            print(cost)
            self.assignment = MIP_Assignment(cost, self.base.weapons, self.base.closest_drones)     ## assign the weapons to the closest drones.
            print(f'assignment.assignement= {self.assignment.assignement}')
            for i in self.assignment.assignement:                                                   ## go through the allocated drones.
                self.base.closest_drones[i[1]].drone_get_destroyed(self.base.closest_drones[i[1]], self.base.weapons[i[0]], self.base, self)         ## fire the allocated drones.
            for k in self.drone_list:                                                               ## update the drone status after the shooting.
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
                for weapon in self.base.weapons:
                    k.drone_escape(weapon, self.base)
            self.downtime_timer += self.time_step
            counter_active = 0
            sum_damage = 0
            for alive in self.drone_list:                                                           ## Count the number of drones alive at each time step.
                if alive.active == 1:
                    counter_active += 1
                    sum_damage += alive.damage
            self.theo_damage.append(sum_damage)

            print(f'time step = {t}')
            print(f'The actual number of drones alive is {counter_active}')                         ## number of UAVs live at time step
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t)
        return self.counter_drones_destroyed, self.score


###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####

#
### Get the weapons ###
# Gun1 = Weapons.Gun('Gun1',50,np.array([False, False]), 10)
# Gun2 = Weapons.Gun('Gun2',50,np.array([False, False]), 10)
# grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
# Laser1 = Weapons.Laser('Laser1',50, np.array([False, False]), 12)
# Laser2 = Weapons.Laser('Laser2',50, np.array([False, False]), 6)
#
# ### Get the initial swarm and all initialize the base ###
# n = 4                 # number of weapons #
# initial_swarm_random = Random(30)
# base_random = GBAD(np.array([0, 0, 0]), initial_swarm_random.drone_list, [Gun1, Gun2, grenade1,
#                                                                      Laser1])
# # initial_swarm = Ball(30, 5, np.array([50,30, 40]), 0.58)
# # base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, grenade1,
# #                                                                      Laser1])
#
# ## Run the simulation ##
#
# sim2 = Sim2(20, 1, base_random)
# number_of_drones_destroyed = sim2.next()[0]
# print(f'GBAD HEALTH = {base_random.health}')
# print(f'SCORE = {sim2.score}')
# print(f'DRONES DESTROYED = {number_of_drones_destroyed}')
# print('*************')
# print(f'Time to kill all drones = {sim2.time_to_kill_everybody} s.')
