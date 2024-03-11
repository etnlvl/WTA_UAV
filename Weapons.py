import Drone
import numpy as np



class Weapons:
    def __init__(self, reward_value, state_dependency ) :
        self.reward_value = 100
        self.state_dependency = state_dependency       ### state_dependency = [Boolean, Boolean] =[succesfully_allocated, succesfully_destroyed_drones]
        self.engaged = False







    def is_avalaible (self, time) :
        return time >= self.last_fired_time + self.reload_time


class Gun(Weapons):
    def __init__(self,name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.63521
        self.transition_value = np.array([[1 - self.Pc],[self.Pc]])
        self.downtime = 0.5
    ammunition = 10000
    rc = 100
    destroy_time = 1
    reach_time = 0.5
    range_window = [0, 100]

class Laser(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.75
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5


    ammunition = 1000  # ammunition remaining
    rc = 45  # maximum range
    destroy_time = 15  # time for the weapon to destroy the target
    reach_time = 0.002  # time for the beam to destroy the target
    range_window = [5,50]

class Grenade(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = np.array([[1],[-1],[-2]])
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.4256
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5
    Pc = 0.4256
    ammunition = 1000
    rc = 35
    range_window = [30, 60]

class Net(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 0.85
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
        self.downtime = 0.5
    ammunition = 1000
    rc = 100

    range_window = [30, 100]


class Jammer(Weapons):
    def __init__(self,name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
        self.engaged = False
        self.Pc = 1
        self.transition_value = np.array([[1 - self.Pc], [self.Pc]])
    ammunition = 1000
    rc = 60
    range_window = [5, 60]


