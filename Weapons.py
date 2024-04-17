import Drone
import numpy as np



class Weapons:
    def __init__(self, reward_value, state_dependency):
        self.reward_value = 100
        self.state_dependency = state_dependency       ### state_dependency = [Boolean, Boolean] =[succesfully_allocated, succesfully_destroyed_drones]
        self.engaged = False

    def find_weapon(self, name, list):
        for weapon in list:
            if getattr(weapon, 'name') == name:
                return weapon


class Gun(Weapons):
    def __init__(self,name, reward_value, state_dependency, ammunition ):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        # self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.635
        self.transition_value = np.array([[1 - self.Pc],[self.Pc]])
        self.downtime = 0.5
        self.ammunition = ammunition
    rc = 100
    destroy_time = 1
    reach_time = 0.5
    range_window = [0, 100]

class Laser(Weapons):
    def __init__(self, name, reward_value, state_dependency, ammunition):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        # self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.80
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5
        self.ammunition = ammunition


    ammunition = 1000  # ammunition remaining
    rc = 45  # maximum range
    destroy_time = 15  # time for the weapon to destroy the target
    reach_time = 0.002  # time for the beam to destroy the target
    range_window = [5,50]

class Grenade(Weapons):
    def __init__(self, name, reward_value, state_dependency, ammunition):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.4256
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5
        self.ammunition = ammunition
    Pc = 0.4256
    ammunition = 1000
    rc = 35
    range_window = [30, 60]

class Net(Weapons):
    def __init__(self, name, reward_value, state_dependency, ammunition):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.85
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5
        self.ammunition = ammunition
    ammunition = 1000
    rc = 100

    range_window = [30, 100]


class Jammer(Weapons):
    def __init__(self,name, reward_value, state_dependency, ammunition):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 1
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.ammunition = ammunition
    rc = 60
    range_window = [5, 60]


