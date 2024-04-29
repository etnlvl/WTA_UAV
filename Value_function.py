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


    def get_value_function_v1(self, target):
        Sr = target.target_survivability
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v1 = (self.static_weights[0] * Sr + self.static_weights[1] * Gr + self.static_weights[2]*Er + self.static_weights[3] * Dr + self.static_weights[4] * Dir)
        return self.V_function_v1

    def get_value_function_v2(self, target):
        Sr = target.target_survivability
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v2 = self.dynamic_weights[2] * Er * (self.dynamic_weights[1] * Gr + self.dynamic_weights[0] * Sr)  * np.exp(
                                                                                                   self.dynamic_weights[3] * Dr + self.dynamic_weights[4]*Dir)
        return self.V_function_v2

    def get_value_function_v3(self, target) :
        Sr = target.target_survivability
        Gr = self.base.health
        Er = target.engagement_zone
        Dr = target.damage
        Dir = target.drone_dist
        self.V_function_v1 = self.static_weights[2] * Er *(self.static_weights[0] * Sr + self.static_weights[1] * Gr +
                              self.static_weights[3] * Dr + self.static_weights[4] * Dir)
        return self.V_function_v1




