class Weapons:
    pass

class Laser(Weapons):
    Pc = 0.5  # probability of hit
    ammunition = 150  # ammunition remaining
    rc = 200  # maximum range
    downtime = 0.5  # time needed for the weapon to be available again
    destroy_time = 15  # time for the weapon to destroy the target
    reach_time = 0.002  # time for the beam to destroy the target
    name = "Laser"

    def __init__(self ):
        pass
class Gun(Weapons):
    Pc = 0.7
    ammunition = 60
    rc = 200
    downtime = 2
    destroy_time = 1
    reach_time = 0.5
    name = "Gun"

    def __init__(self):
        pass


class Net(Weapons):
    Pc = 0.85
    ammunition = 10
    rc = 100
    downtime = None  # seconds
    name = "Net"

    def __init__(self):
        pass

class Jammer(Weapons):
    Pc = 1
    ammunition = 80
    rc = 60
    name = "Jammer"

    def __init__(self):
        pass
class Grenade(Weapons):
    Pc = 0.85
    ammunition = 80
    rc = 60
    name = "Grenade "

    def __init__(self):
        pass
