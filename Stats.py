import Drone as Drones
from Linear_Assignment import Linear_Assignment
from MIP_Assignment import MIP_Assignment
import GBAD
import Weapons
import numpy as np
from math import *
import pandas as pd

class Stats :
    def __init__(self, number_of_drones, st, time_step, weapons_desired, resol_method, nb_sim):
        self.number_of_drones = number_of_drones
        self.st = st
        self.time_step = time_step
        self.weapons_desired = weapons_desired
        self.resol_method = resol_method
        self.nb_sim = nb_sim
        self.total_nb_alive = []
        self.weapons_list = []

    def build_weapon_list (self) :
        for weapon, number in self.weapons_desired.items() :
            for k in range (number):
                # self.weapons_list.append(Weapons.Gun(f'{weapon}{k+1}',100, np.array([False,False])))
                self.weapons_list.append(globals()['Weapons'].__dict__[weapon](weapon, 50, np.array([False,False])))

        return self.weapons_list

    def statistic (self) :
        for k in range (self.nb_sim):
            print(f'SIMULATION {k}')
            initial_swarm = Drones.Ball(self.number_of_drones,5, np.array([50,30,40]),1)
            print('Initial Swarm')
            print(initial_swarm)
            base = GBAD.GBAD(np.array([0,0,0]), initial_swarm.drone_list, self.weapons_list)
            if self.resol_method == 'MDP' :
                from sim_MDP import Sim_MDP
                simu = Sim_MDP(self.st, self.time_step, base)
                self.total_nb_alive.append(simu.next_MDP()[1][-1])
            else :
                from sim2 import Sim2
                simul = Sim2(self.st, self.time_step, base)
                self.total_nb_alive.append(simul.next()[1][-1])

first_stat = Stats(30,5,1,{'Gun':2, 'Grenade' : 1, 'Laser' :2},'MDP',20)
scd_stat = Stats(30,5,1,{'Gun':2, 'Grenade' : 1, 'Laser' :2},'closest',20)
first_stat.build_weapon_list()
first_stat.statistic()
scd_stat.build_weapon_list()
scd_stat.statistic()
df1 = pd.DataFrame(first_stat.total_nb_alive, columns =['Alive MDP'])
df2 = pd.DataFrame(scd_stat.total_nb_alive, columns =['Alive closest process'])

df = pd.concat([df1,df2], ignore_index = True )
df.to_excel('hdehdedh.xlsx', index=False)




