from Drone import Ball
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np
from Drone import Drone
from policy_assignment import Policy


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
        self.weapons_with_ammo = []
        self.score = 0

    "Sim2 and its function Sim2.next() makes run the battle by allocating weapons to targets with the MIP algorithm taken from the library OR tools"

    def next(self):                                                                                 ## This function proceed to the global simulation                    ## Create cost/probability matrix
        random_time_spone = 10  ### at this time, one drone more dangerous will spone in the simulation
        for t in range (0,self.st, self.time_step):                                                 ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f' Time Step = {t}')
            self.weapons_with_ammo = []
            threat_values = [drone.update_TV() for drone in base.drone_list]
            print(f'the threat values of drones are : {threat_values}')
            if t == random_time_spone:
                print(f'THE HEAVY PAYLOAD DRONE IS ENTERING THE SIMULATION')
                tv_max = max(threat_values)
                drone = Policy.find_drone_tv(Policy, tv_max, base.drone_list)
                new_pos = drone.pos + np.array([drone.pos[0]+5, drone.pos[1]+2, drone.pos[2]+12])
                dangerous_drone = Drone(new_pos, len(base.drone_list), None)
                dangerous_drone.threat_val = tv_max + 10
                base.drone_list.append(dangerous_drone)
                threat_values.append(dangerous_drone.threat_val)
                print(f'the threat values of drones are : {threat_values}')

            for weapon in self.base.weapons:
                if weapon.ammunition > 0:
                    self.weapons_with_ammo.append(weapon)
            w_prob = [w.Pc for w in self.weapons_with_ammo]
            if len(w_prob) == 0:
                print('All the weapons are out of ammunitions')
            # print(f'Downtime Timer = {self.downtime_timer}')
            # print(f'The number of weapons with ammo remaining is {len(w_prob)}')
            print(f'{self.weapons_with_ammo[0].ammunition}')
            self.base.get_closest_drones(len(self.weapons_with_ammo))
            cost = np.reshape(np.repeat(w_prob, len(self.weapons_with_ammo)), (len(self.weapons_with_ammo), len(self.weapons_with_ammo)))
            dist = self.base.get_closest_drones(len(self.weapons_with_ammo))[0]                                          ## gets all n-weapons the closest drones to assign it later with the MIP algorithm

            for index, w in enumerate(self.weapons_with_ammo):

                cost[index] = cost[index] * [d < w.rc for d in dist]                                ## set a zero probability in the cost matrix if the drone is out of range of the weapon
                # cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)                 ## set a zero probability in the cost matrix if corresponding weapon has no more ammunitions
                if np.mod(self.downtime_timer, w.downtime) != 0:                                    ## check if  weapon is ready and re-loading.
                    print(f' {w.name} is not available')
                    cost[index] = [0]*len(self.base.get_closest_drones(len(self.weapons_with_ammo)))
            print(cost)
            self.assignment = MIP_Assignment(cost, self.weapons_with_ammo, self.base.closest_drones)     ## assign the weapons to the closest drones.
            for i in self.assignment.assignement:                                                        ## go through the allocated drones.
                self.base.closest_drones[i[1]].drone_get_destroyed(self.weapons_with_ammo[i[0]])         ## fire the allocated drones.
                if self.base.closest_drones[i[1]].active == 0:
                    print(f'the added value to the score is : {self.base.closest_drones[i[1]].threat_val}')
                    self.score += self.base.closest_drones[i[1]].threat_val
            for k in self.drone_list:                                                               ## update the drone status after the shooting.
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step
            counter_active = 0
            for alive in self.drone_list:                                                           ## Count the number of drones alive at each time step.
                if alive.active == 1:
                    counter_active += 1
            # print(f'time step = {t}')
            # print(f'The actual number of drones alive is {counter_active}')                         ## number of UAVs live at time step
            if counter_active == 0:
                break
            self.count_alive.append(counter_active)
            self.the_time_steps.append(t)
        return self.the_time_steps, self.count_alive


###### Import the parameters for the global simulation #####
###Get the initial position and the type of swarm desired#####


### Get the weapons ###
Gun1 = Weapons.Gun('Gun1', 50, np.array([False, False]), 10)
Gun2 = Weapons.Gun('Gun2', 50, np.array([False, False]), 10)
grenade1 = Weapons.Grenade('Grenade1', 50, np.array([False, False]), 7)
Laser1 = Weapons.Laser('Laser1', 50, np.array([False, False]), 12)
Laser2 = Weapons.Laser('Laser2', 50, np.array([False, False]), 6)

### Get the initial swarm and all initialize the base ###
n = 4                 # number of weapons #
initial_swarm = Ball(30, 5, np.array([30,20, 15]), 2)
base = GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])

## Run the simulation ##

sim2 = Sim2(20, 1, base)
final_nb_drones_alive = sim2.next()[1][-1]
print(f'The final number of UAVs alive is : {final_nb_drones_alive}')
print(f'Final score = {sim2.score}')

