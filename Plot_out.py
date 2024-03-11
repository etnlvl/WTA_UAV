import Drone as Drones
from MIP_Assignment import MIP_Assignment
import gbad
import Weapons
import numpy as np
import matplotlib.pyplot as plt
import sim2

class Plot_out :

    def __init__(self, base, time_step):
        self.time_step = time_step
        self.base = base
        self.active_drones = []
        self.time = []



    def plot(self, les_t, les_actives, les_actives2) :
        p1 = plt.plot(les_t, les_actives, marker='v')
        p2 = plt.plot(les_t, les_actives2, marker= "o" )
        plt.title("Total Drones destroyed at time t")
        plt.legend([p1,p2],["For 4 weapons on base","For 6 weapons on base"])
        plt.show()

####### Import the parameters for the global simulation #####
    ####Get the initial position and the type of swarm desired####
initial_swarm = Drones.Ball(30, 5, np.array([5, 5, 4]), 0.58)

### Get the weapons ###
Gun1 = Weapons.Gun()
Gun2 = Weapons.Gun()
grenade = Weapons.Grenade()
Laser1 = Weapons.Laser()
Laser2 = Weapons.Laser()
n = 4  # number of weapons #
base = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2,
                                                                     Laser1, Laser2])
second_base = GBAD.GBAD(np.array([0, 0, 0]), initial_swarm.drone_list, [Gun1, Gun2,grenade,
                                                                     Laser1, Laser2])
time_step = 1
simul = Sim2.Sim2(5, time_step , base)
simul2 = Sim2.Sim2(5,time_step,second_base )
first_plot = Plot_out(base, time_step )

first_plot.plot(simul.next()[0],simul.next()[1], simul2.next()[1])
