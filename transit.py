import numpy as np
import Drone
from gbad import GBAD

class Policy :
    def __init__(self,weapon_idx, n_targets, n_assignments):
        self.weapon_idx = weapon_idx
        self.n_targets = n_targets
        self.n_assignments = n_assignments
        self.weapon_policy = dict()
        self.surv_prob = np.zeros((n_targets, n_assignments+1))
        self.expected_value = np.zeros((n_targets, n_assignments+1))
        self.policy_values = []

    def get_first_policy(self, closest_drones):                             ### it is useless to calculate the value of the first policy
        self.weapon_policy[f'{self.weapon_idx}'] = [0] * self.n_assignments
        for t in range(self.n_assignments):
            self.weapon_policy[f'{self.weapon_idx}'][t] = closest_drones[t]
        return self.weapon_policy

    def initialize_surv_prob(self, first_policy, prob):
        self.surv_prob[:, 0] = np.array(([1]*self.n_targets))
        for t in range(0, self.n_assignments):
            self.surv_prob[:, t+1] = self.surv_prob[:, t]
            self.surv_prob[first_policy['0'][t].idx][t+1] = self.surv_prob[first_policy[f'{self.weapon_idx}'][t].idx-1][t]*(1-prob[0])
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
        for drone in list :
            if getattr(drone, 'idx') == value_index-1:
                return drone
        return None

    def convert_idx_to_object (self, drone_list, index_policy):
        policy_converted = []
        for index in index_policy:
            policy_converted.append(self.find_drone(index, drone_list))
        return policy_converted



    def get_next_policy(self, prob_weapon, S, drone_list):
        next_policy = []
        policy_value = 1
        self.expected_value = S * prob_weapon
        for t in range(self.n_assignments):
            a = np.argmax(self.expected_value[:, t])
            idx_to_pick_randomly = []                                               ### in  the case where there is several values at the same maximum expected_value, we pick randomly one of the corresponding indexes.
            for j in range(self.n_targets):
                if self.expected_value[j][t] == np.max(self.expected_value[:, t]):
                    idx_to_pick_randomly.append(j)                                  # Fix this
            if a not in idx_to_pick_randomly:
                idx_to_pick_randomly.append(a)
            next_policy.append(np.random.choice(idx_to_pick_randomly)+1)
        right_next_policy = self.convert_idx_to_object(drone_list,next_policy)
        for t in range (1,self.n_assignments):        ## to calculate the policy_value
            policy_value = policy_value * prob_weapon * S[next_policy[t]-1][t]

        return next_policy

    def get_all_policies(self, n_weapons, prob_weapons, drone_list):
        for i in range(1, n_weapons):
            self.weapon_policy[f'{self.weapon_idx + i}'] = self.convert_idx_to_object(drone_list, self.get_next_policy(prob_weapons[i], self.surv_prob, drone_list))
            self.update_surv_prob(prob_weapons[i], self.weapon_policy[f'{i}'])
        return self.weapon_policy










