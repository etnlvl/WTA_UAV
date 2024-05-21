### Importing all the necessary packages. ###

import numpy as np
import heapq as hp


"This file retains all the important informations we need for the simulation about the base defense system such as its health bar,"
"the number of weapons in operating state, etc."

class GBAD:
    def __init__(self, position, drone_list, weapons_list):
        self.position = position                                                # Define the position of the base.
        self.drone_list = drone_list                                            # Get the drone list.
        self.closest_drones = []                                                # Get the closest drones list.
        self.highest_TV_drones = []                                             # Get the most dangerous drones list.
        self.weapons = weapons_list                                             # Get the weapon list.
        self.nw = len(weapons_list)
        self.n_drone = len(drone_list)
        self.alive_drones = []                                                  # Get the alive drones list
        self.health = 1                                                         # Set the GBAD health bar at one at the beginning of the simulation

### Function to get all the distances between the base and every single drone of the swarm ###
    def get_distance_drone(self):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        for idx, d in enumerate(self.drone_list):
            d.drone_dist = a[idx]
        return a

### Function to get the list of all the drones alive ###
    def get_all_live_drones(self):
        live_drones = [d for d in self.drone_list if d.active == 1]
        self.alive_drones = live_drones
        return self.alive_drones

### Function to get the list of all the most dangerous drones ###
    def get_highest_TV_drones(self, n):
        a = [d.threat_val for d in self.drone_list]
        highest = hp.nlargest(n, a)
        indexes = [a.index(t) for t in highest]
        self.highest_TV_drones = [self.drone_list[idx] for idx in indexes]
        return highest, self.highest_TV_drones

### Function to get the list of the closest drones ###
    def get_closest_drones(self, n):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        n_dist = hp.nsmallest(n, a)
        indexes = [a.index(t) for t in n_dist]
        self.closest_drones = [self.drone_list[idx] for idx in indexes]
        return n_dist, self.closest_drones





