from Drone import Random
from MIP_Assignment import MIP_Assignment
from gbad import GBAD
import Weapons
import numpy as np
from Drone import Drone
from policy_assignment import Policy
"This file define the first simulator created using the MIP assignment module of OR-tools library"
"In this simulator, an update and an assignment were made at each single time step of the simulation. "
"All the necessary variables useful to run this file are imported from the other scripts Drone, gbad, Weapons etc.  "

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
        self.counter_drones_destroyed =0
        self.targets_alive_ts = []
        self.GBAD_health_state = []
        self.theo_damage = []
        self.surv_weapons = {'Gun1': [], 'Gun2': [], 'Grenade1': [], 'Laser1': []}
        self.score = 0
        self.next()

    "Sim2 and its function Sim2.next() makes run the battle by allocating weapons to targets with the MIP algorithm taken from the library OR tools"

    def next(self):                                                                                 ## This function proceed to the global simulation                    ## Create cost/probability matrix
        for t in range (0,self.st, self.time_step):                                                 ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            print(f' Time Step = {t}')
            ### Creating the list of weapons with ammos
            self.weapons_with_ammo = []
            self.GBAD_health_state.append(self.base.health)
            for weapon in self.base.weapons:
                if weapon.ammunition > 0:
                    self.weapons_with_ammo.append(weapon)
            ### Creating the list of the corresponding probabilities of kill for these weapons.
            w_prob = [w.Pc for w in self.weapons_with_ammo]
            print(f'the list to build the cost matrix is this shit  :{np.repeat(w_prob, len(self.weapons_with_ammo))}')
            if len(w_prob) == 0:
                print('All the weapons are out of ammunitions')
                break


            print(f'Number of ammos for the first weapon of the list : {self.weapons_with_ammo[0].ammunition}')

            cost = np.reshape(np.repeat(w_prob, len(self.weapons_with_ammo)), (len(self.weapons_with_ammo), len(self.weapons_with_ammo)))

            dist2 = self.base.get_closest_drones(len(self.weapons_with_ammo))[1]
            print(f'dist2 = {[element.threat_val for element in dist2]}')
            dist3 = [np.linalg.norm(np.array([0,0,0]) - drone.pos) for drone in dist2]
            print(f'dist3 = {dist3}')
            self.targets_alive_ts.append(self.nbd - self.counter_drones_destroyed)
            for index, w in enumerate(self.weapons_with_ammo):

                cost[index] = cost[index] * [w.range_window[0] <= d <= w.range_window[1] for d in dist3]                                ## set a zero probability in the cost matrix if the drone is out of range of the weapon
                # cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)                 ## set a zero probability in the cost matrix if corresponding weapon has no more ammunitions
                if np.mod(self.downtime_timer, w.downtime) != 0:                                    ## check if  weapon is ready and re-loading.
                    print(f' {w.name} is not available')
                    cost[index] = [0]*len(self.base.get_closest_drones(len(self.weapons_with_ammo)))
            print(f'The cost is {cost}')
            self.assignment = MIP_Assignment(cost, self.weapons_with_ammo, self.base.highest_TV_drones)     ## assign the weapons to the closest drones.
            for i in self.assignment.assignement:                                                        ## go through the allocated drones.
                self.base.closest_drones[i[1]].drone_get_destroyed(self.base.closest_drones[i[1]], self.weapons_with_ammo[i[0]], self.base, self)         ## fire the allocated drones.

            for k in self.drone_list:                                                               ## update the drone status after the shooting.
                if k.active == 1:
                    k.update_drone_pos(self.time_step)
            self.downtime_timer += self.time_step


        return  self.counter_drones_destroyed, self.score


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
random_swarm = Random(100, 60)
base = GBAD(np.array([0, 0, 0]), random_swarm.drone_list, [Gun1, Gun2, grenade1,
                                                                     Laser1])

## Run the simulation ##

sim2 = Sim2(60, 1, base)
print(f'GBAD HEALTH = {base.health}')
print(f'SCORE = {sim2.score}')
print(f'DRONES DESTROYED = {sim2.targets_alive_ts}')
