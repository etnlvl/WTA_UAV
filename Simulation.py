import Drone
from Linear_Assignment import Linear_Assignment
from MIP_Assignment import MIP_Assignment
import GBAD
import Weapons
import Drone
import numpy as np


class Simulation:

    def __init__(self, st, nbd, nbw, time_step, drone_list):
        self.st = st
        self.nbd = nbd
        self.nbw = nbw
        self.time_step = time_step
        self.drone_list = drone_list
        self.base = None



    ####### Import the parameters for the global simulation #####
    ####Get the initial position and the type of swarm desired#####
    initial_swarm = Drone.Ball(20,50,np.array([10,10,4]),3).get_ini_pos_ball()

    ### Get the weapons ###
    Gun1 = Weapons.Gun()
    Gun2 = Weapons.Gun()
    grenade = Weapons.Grenade()
    Laser1 = Weapons.Laser()
    Laser2 = Weapons.Laser()
    n = 5                  # number of weapons #
    ### Get the base under attack ###
    base = GBAD.gbase

    def simu (self) :
        # Get probabilities of weapons
        w_prob = [w.Pc for w in self.base.weapons]
        # Create cost/probability matrix
        cost = np.reshape(np.repeat(w_prob, self.n), (self.base.nw, self.n))
        for t in range (0,self.st, self.time_step) :                        ## for the all simulation time, from t=0s to ts = time_simulation increased by t = time_step ##
            self.base.get_closest_drones(self.n)
            print(self.base)
            for index, w in enumerate(self.base.weapons):
                print('TEST')
                dist = self.base.get_closest_drones(self.n)  # Get closest drones
                cost[index] = cost[index] * [d < w.rc for d in dist]
                cost[index] = cost[index] * np.repeat([w.ammunition > 0], self.n)
            print(MIP_Assignment(cost).optimizeMIP())
            if MIP_Assignment(cost).optimizeMIP() == "No solution found." :                   ### it is impossible to allocate any weapon to any target at this time step, so we make the all drones keep moving forward ####
                for k in range (0,self.nbd) :
                    self.drone_list[k].Drone.update_drone_pos(self,t)                         ### Update the position of each drone in the swarm, the closest and all others
            else :                                                                            ### we try to kill the closest drones
                alloc = MIP_Assignment.optimizeMIP()
                print(alloc)
                for l in range (len(alloc)) :
                    closest_idx = self.base.closest_drones() # Closest drones indexes
                    closest_idx[alloc]
            ## then, update the position of drones
            for k in range (len(self.drone_list)):
                update_drone_pos











    # update position at time step #
    # drone.update_drone_pos(self.time_step)



