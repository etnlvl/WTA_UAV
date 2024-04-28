import numpy as np
import Drone
from gbad import GBAD

class Policy :
    def __init__(self,weapon_set, n_targets, n_assignments):
        self.weapon_set = weapon_set        ##### [Gun1, Gun2, Grenade1, Laser1]
        self.n_targets = n_targets
        self.n_assignments = n_assignments
        self.weapon_policy = dict()
        self.surv_prob = np.zeros((n_targets, n_assignments+1))
        self.expected_value = np.zeros((n_targets, n_assignments+1))
        self.policy_values = []
        self.first_weapon_ammun = None                                          ### the first weapon which has ammunition to build the policy

    def get_first_policy(self, highest_TV_drones):                              ### it is useless to calculate the value of the first policy
        print(f'the weapon_set before the loop is {[weapon.name for weapon in self.weapon_set]}')
        new_weapon_set =[]
        for weapon in self.weapon_set:
            print(f'{weapon.name} has {weapon.ammunition} ammos')
            if weapon.ammunition > 0:
                new_weapon_set.append(weapon)
        self.weapon_set = new_weapon_set
        print(f'the weapon_set after the loop is {[weapon.name for weapon in self.weapon_set]}')
        if len(self.weapon_set) == 0:
            print('All the weapons are out of ammunitions')
            return None
        self.weapon_policy[self.weapon_set[0].name] = [0] * self.n_assignments
        print(f' The first weapon for the first policy is {self.weapon_set[0].name} and has {self.weapon_set[0].ammunition} ammo ')
        for t in range(self.n_assignments):
            self.weapon_policy[self.weapon_set[0].name][t] = highest_TV_drones[t]
            print(highest_TV_drones[t].idx)


        return self.weapon_policy


    def initialize_surv_prob(self, first_policy, prob):
        if first_policy == None :
            return None
        else:
            self.surv_prob[:, 0] = np.array(([1]*self.n_targets))
            for t in range(0, self.n_assignments):
                self.surv_prob[:, t+1] = self.surv_prob[:, t]
                self.surv_prob[first_policy[self.weapon_set[0].name][t].idx][t+1] = self.surv_prob[first_policy[self.weapon_set[0].name][t].idx-1][t]*(1-prob[0])
            self.surv_prob = np.delete(self.surv_prob, 0, axis=1)
        return self.surv_prob

    def update_surv_prob(self, prob, policy):
        for n in range(0, self.n_assignments):
            if n==0:
                self.surv_prob[policy[n].idx-1][n] = \
                self.surv_prob[policy[n].idx-1][n] * (1 - prob)
            else :
                self.surv_prob[policy[n].idx - 1][n] = \
                    self.surv_prob[policy[n].idx - 1][n-1] * (1 - prob)
        return self.surv_prob

    def find_drone(self, value_index, list):
        for drone in list:
            if getattr(drone, 'idx') == value_index-1:
                return drone

    def find_drone_tv(self, threat_value, list):
        for drone in list :
            if getattr(drone , 'threat_val') == threat_value:
                return drone

    def convert_idx_to_object(self, drone_list, index_policy):
        policy_converted = []
        for index in index_policy:
            policy_converted.append(self.find_drone(index, drone_list))
        return policy_converted


    def get_next_policy(self, prob_weapon, S, drone_list):
        next_policy = []
        policy_value = 1
        for j in range(self.n_targets):
            for t in range(self.n_assignments):
                self.expected_value[j][t] = prob_weapon * S[j][t]
        for t in range(self.n_assignments):
            a = np.argmax(self.expected_value[:, t])
            idx_to_pick_randomly = []        ### in  the case where there is several values at the same maximum expected_value, we pick randomly one of the corresponding indexes.
            for j in range(self.n_targets):
                if self.expected_value[j][t] == np.max(self.expected_value[:, t]):
                    idx_to_pick_randomly.append(j) # Fix this
            if a not in idx_to_pick_randomly:

                idx_to_pick_randomly.append(a)
            next_policy.append(np.random.choice(idx_to_pick_randomly)+1)
        right_next_policy = self.convert_idx_to_object(drone_list,next_policy)
        for t in range (1,self.n_assignments):        ## to calculate the policy_value
            policy_value = policy_value * prob_weapon * S[next_policy[t]-1][t]

        return next_policy

    def get_all_policies(self, alive_drone_list, drone_list):
        for weapon in self.weapon_set:
            if weapon.ammunition > 0 and (weapon.name not in self.weapon_policy.keys()):
                # print(f'OVERWRITTING {self.weapon_policy.keys()}')
                # print(f' ammo of weapon {weapon.ammunition}')
                self.weapon_policy[weapon.name] = self.convert_idx_to_object(drone_list, self.get_next_policy(weapon.Pc, self.surv_prob, alive_drone_list))

                self.update_surv_prob(weapon.Pc, self.weapon_policy[weapon.name])


        return self.weapon_policy










