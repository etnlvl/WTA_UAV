from Drone import Drone
from Drone import Ball
from gbad import GBAD
import Weapons
import numpy as np


class Feed_MIP :
    def __init__(self, weapons, targets, base, weights):
        self.weapons = weapons
        self.targets = targets
        self.base = base
        self.static_weights = weights   # [alpha, beta, gamma, phi, lambda]
        self.dynamic_weights = weights
        self.V_function_v1 = 0
        self.V_function_v2 = 0


    def get_value_function_v1(self, target, weapon, simu):
        Sr = simu.surv_weapons[weapon.name][target.idx]
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        print(f'Variable values for target :{target.idx}')
        print(f'Sr = {Sr}')
        print(f'Gr= {Gr}')
        print(f'Er= {Er}')
        print(f'Dr={Dr}')
        print(f'Dir= {Dir}')
        self.V_function_v1 = self.static_weights[0] * Sr + self.static_weights[1]*weapon.Pc +  self.static_weights[1]*Gr +self.static_weights[2]*Er + self.static_weights[3] * Dr + self.static_weights[4] * (1-Dir)
        print(f' Vf()= {self.V_function_v1}')
        return self.V_function_v1, Sr, Gr, Er, Dr, Dir

    def get_value_function_v2(self, target, weapon, simu):
        Sr = simu.surv_weapons[weapon.name][target.idx]
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v2 = ((self.static_weights[2]*Er+ self.static_weights[3]*Dr)**3)*np.exp(self.static_weights[0]*Sr + self.static_weights[4]*Dir + self.static_weights[1]*Gr)
        return self.V_function_v2

    def get_value_function_v3(self, target) :
        Sr = target.target_survivability
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v3 = self.static_weights[2] * Er *(self.static_weights[0] * Sr + self.static_weights[1] * Gr +
                              self.static_weights[3] * Dr + self.static_weights[4] * Dir)
        return self.V_function_v3

    def get_value_function_v4(self, target) :
        Sr = target.target_survivability
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v4 = self.static_weights[2] * Er *(self.static_weights[0] * Sr + self.static_weights[1] * Gr +
                              self.static_weights[3] * Dr + self.static_weights[4] * Dir)
        return self.V_function_v4


