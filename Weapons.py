import Drone



class Weapons:
    def __init__(self, reward_value, state_dependency) :
        self.reward_value = reward_value
        self.state_dependency = state_dependency       ### state_dependency = [Boolean, Boolean] =[succesfully_allocated, succesfully_destroyed_drones]




    def update_drone_status (self, weapon) :
        return Drone.drone_get_destroyed(self, weapon)

class Laser(Weapons):
    def __init__(self, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value

    Pc = 0.5  # probability of hit
    ammunition = 150  # ammunition remaining
    rc = 200  # maximum range
    downtime = 0.5  # time needed for the weapon to be available again
    destroy_time = 15  # time for the weapon to destroy the target
    reach_time = 0.002  # time for the beam to destroy the target
    name = "Laser"


class Gun(Weapons):
    def __init__(self, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
    Pc = 0.7
    ammunition = 60
    rc = 200
    downtime = 2
    destroy_time = 1
    reach_time = 0.5
    name = "Gun"


class Net(Weapons):
    def __init__(self, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
    Pc = 0.85
    ammunition = 10
    rc = 100
    downtime = None  # seconds
    name = "Net"

class Jammer(Weapons):
    def __init__(self, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
    Pc = 1
    ammunition = 80
    rc = 60
    name = "Jammer"
class Grenade(Weapons):
    def __init__(self, reward_value, state_dependency):
        super().__init__(reward_value, state_dependency)
        self.state_dependency = state_dependency
        self.reward_value = reward_value
    Pc = 0.85
    ammunition = 80
    rc = 60
    name = "Grenade "
    downtime = 1.5
