import numpy as np
import heapq as hp
from Try import Bellman
import matplotlib.pyplot as plt
import Drone
import Weapons2
class GBAD:
    def __init__(self, position, drone_list, weapons_list):
        self.position = position
        self.drone_list = drone_list
        self.closest_drones = []
        self.weapons = weapons_list
        self.nw = len(weapons_list)
        self.n_drone = len(drone_list)
        self.alive_drones = []
        # self.bellman = Bellman(n_states = 1, n_actions = self.nw, discount_factor= discount_factor)



        # self.state = None
        # self.action = None
        # self.reward = None

    def get_distance_drone(self):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        for idx, d in enumerate(self.drone_list):
            d.drone_dist = a[idx]
        return a

    def get_all_live_drones(self):
        live_drones = [d for d in self.drone_list if d.active == 1]
        self.alive_drones = live_drones
        return self.alive_drones

    def get_closest_drones(self, n):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        n_dist = hp.nsmallest(n, a)
        indexes = [a.index(t) for t in n_dist]
        self.closest_drones = [self.drone_list[idx] for idx in indexes]
        return self.closest_drones

    def create_weapons(self):
        pass


## create the drones
# n_drones = 10
# initial_swarm = Drone.Ball(10, 5, np.array([50, 30, 40]), 0.58)
# drones = initial_swarm.drone_list
#




