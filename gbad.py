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
        self.highest_TV_drones = []
        self.weapons = weapons_list
        self.nw = len(weapons_list)
        self.n_drone = len(drone_list)
        self.alive_drones = []


    def get_distance_drone(self):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        for idx, d in enumerate(self.drone_list):
            d.drone_dist = a[idx]
        return a

    def get_all_live_drones(self):
        live_drones = [d for d in self.drone_list if d.active == 1]
        self.alive_drones = live_drones
        return self.alive_drones

    def get_highest_TV_drones(self, n):
        a = [d.threat_val for d in self.drone_list]
        highest = hp.nlargest(n, a)
        indexes = [a.index(t) for t in highest]
        self.highest_TV_drones = [self.drone_list[idx] for idx in indexes]
        return highest, self.highest_TV_drones



    def get_closest_drones(self, n):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        n_dist = hp.nsmallest(n, a)
        indexes = [a.index(t) for t in n_dist]
        self.closest_drones = [self.drone_list[idx] for idx in indexes]
        return n_dist, self.closest_drones

    def create_weapons(self):
        pass




