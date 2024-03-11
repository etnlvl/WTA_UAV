import numpy as np
from Weapons2 import Weapon


class Policy :
    def __init__(self,weapon_idx, n_targets, n_assignments):
        self.weapon_idx = weapon_idx
        self.n_targets = n_targets
        self.n_assignments = n_assignments
        self.weapon_policy = dict()
        self.surv_prob = np.zeros((n_targets, n_assignments+1))
        self.expected_value = np.zeros((n_targets, n_assignments+1))



    def get_first_policy(self):
        self.weapon_policy[f'{self.weapon_idx}'] = [0] * self.n_assignments
        for t in range (self.n_assignments) :
            self.weapon_policy[f'{self.weapon_idx}'][t] = np.random.randint(1,self.n_targets)
        return self.weapon_policy

    def initialize_surv_prob (self, first_policy, prob) :
        self.surv_prob[:,0] = np.array(([1, 1, 1, 1]))
        for t in range (1,self.n_assignments) :
            for j in range (self.n_targets) :
                if first_policy[f'{self.weapon_idx}'][t]== j :
                    self.surv_prob[j][t] = self.surv_prob[j][t-1]*(1-prob[0])
                else :
                    self.surv_prob[j][t] = self.surv_prob[j][t - 1]
        return self.surv_prob

    def update_surv_prob(self, prob, policy) :
        for t in range (1,self.n_assignments) :
            for j in range (self.n_targets) :
                if policy[f'{self.weapon_idx}'][t]== j :
                    self.surv_prob[j][t] = self.surv_prob[j][t-1]*(1-prob)
                else :
                    self.surv_prob[j][t] = self.surv_prob[j][t - 1]
        return self.surv_prob


    def get_next_policy(self, prob_weapon , S) :
        next_policy = []
        for j in range(self.n_targets) :
            for t in range (self.n_assignments) :
                self.expected_value[j][t] = prob_weapon* S[j][t]
        print(self.expected_value)
        for t in range(self.n_assignments) :
            a = np.argmax(self.expected_value[:,t])
            idx_to_pick_randomly = []
            for j in range (self.n_targets) :
                if self.expected_value[j][t] == np.max(self.expected_value[:,t]) :
                    idx_to_pick_randomly.append(j)
            if a not in idx_to_pick_randomly :
                idx_to_pick_randomly.append(a)
            next_policy.append(np.random.choice(idx_to_pick_randomly)+1)
        return next_policy

    def get_all_policies (self, n_weapons, prob_weapons) :
        for i in range (1, n_weapons) :
            self.weapon_policy[f'{self.weapon_idx + i}'] = self.get_next_policy(prob_weapons[i], self.surv_prob)
            print(self.get_next_policy(prob_weapons[i], self.surv_prob))
            print(self.surv_prob)
            self.update_surv_prob(prob_weapons[i],self.weapon_policy)
        return self.weapon_policy


first_policy = Policy(0,4,5)
policy = first_policy.get_first_policy()

first_policy.initialize_surv_prob(policy,[0.85,0.76,0.52])
print(policy)
print(first_policy.surv_prob)

all_policies = first_policy.get_all_policies(3,[0.85,0.76,0.52])
print(all_policies)










