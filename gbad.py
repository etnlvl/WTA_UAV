import numpy as np
import heapq as hp
from Try import Bellman
import matplotlib.pyplot as plt
import Drone
import Weapons2
import Bellman
class GBAD:
    def __init__(self, position, drone_list, weapons_list, discount_factor):
        self.position = position
        self.drone_list = drone_list
        self.closest_drones = []
        self.weapons = weapons_list
        self.nw = len(weapons_list)
        self.n_drone = len(drone_list)
        self.bellman = Bellman(n_states = 1, n_actions = self.nw, discount_factor= discount_factor)



        self.state = None
        self.action = None
        self.reward = None

    def get_distance_drone(self) :
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        for idx, d in enumerate(self.drone_list) :
            d.drone_dist = a[idx]
        return a

    def get_closest_drones(self, n):
        a = [np.linalg.norm(self.position - d.pos) for d in self.drone_list]
        n_dist = hp.nsmallest(n, a)
        indexes = [a.index(t) for t in n_dist]
        self.closest_drones = [self.drone_list[idx] for idx in indexes]
        return n_dist

    def create_weapons(self):
        pass

    def get_drones(self, state) :
        initial_swarm = Drone.Ball(25, 5, np.array([50, 30, 40]), 0.58)
        dronnes = initial_swarm.drone_list
        drones = []
        for i in range(len(bin(state)[2:])) :
            if bin(state)[2:][-i-1] == '1' :
                drones.append(dronnes[i])
        return drones

    def allocate_weapons_to_drones(self, state, drones):
        # Iterate on each weapon and select the closest drone who has not been allocated yet.
        for weapon in self.weapons:
            closest_drone = None
            closest_distance = float('inf')
            for drone in drones:
                # Check if the drone has not been allocated to a weapon yet
                if not drone.allocated:
                    # Calculate the distance between the drone and the weapon
                    distance = np.sqrt(
                        drone.pos[0] ** 2 + drone.pos[1] ** 2 + drone.pos[2] ** 2)
                    # Check if the drone is closer than the actual closest drone.
                    if distance < closest_distance:
                        closest_drone = drone
                        closest_distance = distance
            # Allocate the weapon to the closest drone.
            if closest_drone is not None:
                closest_drone.allocated = True
                closest_drone.weapon = weapon



    def compute_transition_model(self):
        n_drones = len(self.drone_list)
        n_states = 2**n_drones
        n_actions = self.nw
        transition_model = np.zeros((n_states, n_actions, n_states))
        for state in range (n_states) :
            drones = self.get_drones(state)
            Drone.Drone.update_drone_pos(drones)
            for action in range (n_actions) :
                next_drones = self.allocate_weapons_to_drones(drones, action)
                next_state = self.get_state(next_drones)
                transition_model[state, action, next_state] = 1.0
        return transition_model

    def compute_reward_model(self):
        n_drones = len(self.drone_list)
        n_states = 2 ** n_drones
        n_actions = self.nw
        reward_model = np.zeros((n_states, n_actions, n_states))
        for state in range(n_states):
            drones = self.get_drones(state)
            for action in range(n_actions):
                next_drones = self.allocate_weapons_to_drones(drones, action)
                next_state = self.get_state(next_drones)
                reward = self.get_reward(state, action, next_state)
                reward_model[state, action, next_state] = reward
        return reward_model


    def get_reward(self, state, action, next_state) :
        drones = self.get_drones(state)
        next_drones = self.get_drones(next_state)
        weapon = self.weapons[action]
        reward = 0
        for drone in drones :
            if drone not in next_drones :
                if weapon.was_last_allocated_to_drone(drone) :
                    reward += 1
                else :
                    pass
            else :
                if weapon.was_last_allocated_to_drone(drone) :
                    if weapon.missed_drone(drone) :
                        reward += 0.5
                    elif weapon.let_drone_escape(drone) :
                        reward += -1
        return reward


    def get_state(self, drones):
        drone_string = ''.join(['{}-{}-{}'.format(drone.idx, drone.pos[0], drone.pos[1], drone.pos[2]) for drone in drones])
        weapon_string = ''.join(
            ['{}-{} '.format(weapon.name, weapon.downtime) for weapon in
             self.weapons])
        state_string = drone_string + weapon_string  ###concatenate to get the actual system's state.
        state_hash = hash(state_string)                #### convert to hash to get an int which represents the actual system's state
        return state_hash

    def remove (self, drone) :
        state = self.get_state(drone)
        state_binary = bin(state)[2:].zfill(self.n_drones)
        state_binary_list = list(state_binary)
        drone_index = drone.id
        state_binary_list[drone_index] = '0'
        new_state_binary = ''.join(state_binary_list)
        new_state = int(new_state_binary, 2)
        return new_state


    def take_action(self,action, drones) :
        weapon = self.weapons[action]        # select the weapon corresponding to the selected action
        ### check if weapon is available
        if weapon.cool_down == 0 :
            ## find the closest drone of the weapon
            closest_drone = min(drones, key = lambda drone: np.sqrt(drone.pos[0]**2 + drone.pos[1]**2 + drone.pos[2]**2))

            ## check if drone in range of the weapon
            if np.sqrt(closest_drone.pos[0]**2 + closest_drone.pos[1]**2 + closest_drone.pos[2]**2) <= weapon.range :
                # Fire
                if np.random.rand () < weapon.p_kill * (1 - np.sqrt(
                        closest_drone.pos[0] ** 2 + closest_drone.pos[1] ** 2 +
                                closest_drone.pos[2] ** 2) / weapon.range):
                    closest_drone.pos = np.array([np.inf, np.inf, np.inf])
                    self.reward += 1
                else :
                    self.reward += -1

                ## update the reload_time of the weapon
                weapon.cool_down = weapon.reload_time
            else :
                ## give a heavier negative reward to the weapon for firring on a drone out of its range
                self.reward += -2
        else :
            self.reward += -3  ### give a heavier negative reward to the weapon for trying to fire while its upload time



### create the drones
n_drones = 10
initial_swarm = Drone.Ball(10, 5, np.array([50, 30, 40]), 0.58)
drones = initial_swarm.drone_list

### create weapons
n_weapons = 3

weapons = [Weapons2.Weapon(1, 30, 0.70, 2),
           Weapons2.Weapon(2, 25, 0.65, 0.5),
           Weapons2.Weapon(3, 50, 0.82, 1)]

### create the base
discount_factor = 0.9
base = GBAD(np.array([0,0,0]),drones, weapons, discount_factor)

### Calculate the optimal value function et the optimal policy
n_iterations = 1000
for i in range(n_iterations) :
    state = base.get_state(drones )
    action = base.bellman.policy
    reward = base.take_action(action, drones)
    base.upda





