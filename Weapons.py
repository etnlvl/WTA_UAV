import Drone



class Weapons:
    def __init__(self, reward_value, state_dependency) :
        self.reward_value = 100
        self.state_dependency = state_dependency       ### state_dependency = [Boolean, Boolean] =[succesfully_allocated, succesfully_destroyed_drones]




    def update_drone_status (self, weapon) :
        return Drone.drone_get_destroyed(self, weapon)


class Gun(Weapons):
    def __init__(self,name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
    Pc = 0.63521
    ammunition = 10000
    rc = 100
    downtime = 0.5
    destroy_time = 1
    reach_time = 0.5
    range_window = [0, 100]

class Laser(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0

    Pc = 0.75  # probability of hit
    ammunition = 1000  # ammunition remaining
    rc = 45  # maximum range
    downtime = 0.5  # time needed for the weapon to be available again
    destroy_time = 15  # time for the weapon to destroy the target
    reach_time = 0.002  # time for the beam to destroy the target
    range_window = [5,50]

class Grenade(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
    Pc = 0.4256
    ammunition = 1000
    rc = 35
    downtime = 0.5
    range_window = [30, 60]

class Net(Weapons):
    def __init__(self, name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
    Pc = 0.85
    ammunition = 1000
    rc = 100
    downtime = None  # seconds
    range_window = [30, 100]


class Jammer(Weapons):
    def __init__(self,name, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
        self.name = name
        self.miss_counter = 0
    Pc = 1
    ammunition = 1000
    rc = 60
    range_window = [5, 60]


