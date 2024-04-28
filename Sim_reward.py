import Drone as Drones
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np

"Sim_Reward and its function next_reward makes run the battle by allocating weapons to targets still with am MIP algorithm but this time a reward is assigned to weapons. "
"Thus, the purpose of this algorithm is to imitate the Markov Decision Process but at the same time, it stays as a greedy algorithm since assignments are made at each single time step "

class Sim_Reward:

    def __init__(self, st, time_step, base):
        self.st = st                                # End time in simulation
        self.nbd = len(base.drone_list)             # Number of drones
        self.time_step = time_step                  # Period of time for the assignment
        self.drone_list = base.drone_list           # takes from GBAD the drone list, it contains position, indexes...
        self.base = base
        self.n = len(self.drone_list)               # Number of Weapons
        self.assignment = None                      # initialize the assignment at nothing at the beginning of the simulation
        self.downtime_timer = 0                     # Counter in order to measure if weapon is available regarding its downtime
        self.count_alive = [len(base.drone_list)]   # list which retains the number of drones alive at each time step.
        self.the_time_steps = [0]

    def next_reward(self):                                                                                              ## This function proceed to the global simulation
        w_prob = [w.Pc for w in self.base.weapons]
        for t in np.arange (0,self.st, self.time_step):                                                                 ## For the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f'Downtime Timer = {self.downtime_timer}')
            dist = self.base.get_distance_drone()                                                                       ## Gets the distance of all drone to the base instead of getting only the closest ones
            cost = np.reshape(np.repeat(w_prob, self.n), (self.base.nw, self.n))
            for index, w in enumerate(self.base.weapons):
                print(f'The enumerate function is going through {self.base.weapons}')
                print(w.reward_value)
                cost[index] = cost[index] * [w.range_window[0] <= d <= w.range_window[1] for d in dist]
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)
                print(f'cost matrix is actually like this {cost}')
                print(f'The element we try to set is like this {cost[index]}')
                print(f'The reward value of this the weapon is {w.reward_value}')
                cost[index] = [w.reward_value * element for element in cost[index]]

                if np.mod(self.downtime_timer, w.downtime) != 0:                                                        ## Means that weapon is not  available
                    cost[index] = [0]*self.n
            self.assignment = MIP_Assignment(cost, self.base.weapons, self.base.drone_list)
            indexes_alloc_weapons = [tup[0] for tup in self.assignment.assignement]
                                                                                                                        ## First allocation is made, we have to check the environment's state  to build the next state
                                                                                                                        ## Checking if the drone has been allocated and updating the corresponding weapon status
            for id, w in enumerate(self.base.weapons):
                if id in indexes_alloc_weapons :
                    w.state_dependency[0] = True
                    self.drone_list[id].drone_allocated.append(w.name)

                                                                                                                        ## Checking if the drone has been effectively destroyed and updating the status (through the function drone_get_destroyed)  ##
            for i in self.assignment.assignement:
                if self.base.drone_list[i[1]].drone_get_destroyed(self.base.weapons[i[0]]):
                    self.base.weapons[i[0]].state_dependency[1] = True
                    self.base.weapons[i[0]].reward_value += 1
                else :
                    self.base.weapons[i[0]].reward_value += -1                                                          ## Give to weapon a negative reward if the drone is miss
                    print(f'{self.base.weapons[i[0]].name} receive a negative reward')
            for drone in self.base.drone_list:                                                                          ## Give a heavier negative reward if one drone escapes from one weapon window_range
                for weapons in self.base.weapons:
                    if drone.drone_escape(weapons) and drone.active == 1:
                        weapons.reward_value += -3
                        print(f'{weapons.name} receive a HEAVY negative reward')

            for agent in self.base.weapons :
                print(f'REWARD VALUE OF {agent.name}={agent.reward_value}')
            for k in self.drone_list:                                                                                   ## Update the drone position if it's still alive
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step
            counter_active = 0
            for alive in self.drone_list:                                                                               ## Count the number of targets alive at the end of the simulation
                if alive.active == 1:
                    counter_active += 1
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t+1)

        return self.the_time_steps, self.count_alive

###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####
n = 4                                                                                                                   ## Number of weapons

### Get the weapons for the first base ###
Gun1 = Weapons.Gun('Gun1',50,np.array([False, False]))
Gun2 = Weapons.Gun('Gun2',50,np.array([False, False]))
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]))
Laser1 = Weapons.Laser('Laser1',50, np.array([False, False]))
Laser2 = Weapons.Laser('Laser2',50, np.array([False, False]))

### Get the initial swarm and initialize the base ###
initial_swarm = Drones.Ball(30, 5, np.array([50,30, 40]), 0.58)
base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])

### Run the Simulation ###

simulation = Sim_Reward(20, 1, base)
final_nb_drones_alive = simulation.next_reward()[1]
print(f'The final number of UAVs alive is : {final_nb_drones_alive}')



