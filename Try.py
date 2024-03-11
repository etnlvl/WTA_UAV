import numpy as np
import Drone as Drones
import Weapons2
import gbad
from MIP_Assignment import MIP_Assignment

class Bellman:
    def __init__(self,n_states, n_actions, discount_factor) :
        self.n_states = n_states
        self.n_actions = n_actions
        self.discount_factor = discount_factor
        self.value_function = np.zeros(n_states)
        self.policy = np.zeros(n_states, dtype = np.int32)

    def compute_value_function(self, transition_model, reward_model):
        while True:
            delta = 0.0
            for state in range(self.n_states):
                action_values = [self.get_action_value(state, action, transition_model, reward_model) for action in range(self.n_actions)]
                best_action_value = max(action_values)
                old_value = self.value_function[state]
                self.value_function[state] = best_action_value
                self.policy[state] = np.argmax(action_values)
                delta = max(delta, abs(old_value - best_action_value))
            if delta < 1e-6:
                break

    def get_action_value(self, state, action, transition_model, reward_model):
        action_value = 0.0
        for next_state, prob in enumerate(transition_model[state, action]):
            reward = reward_model[state, action, next_state]
            action_value += prob * (reward + self.discount_factor * self.value_function[next_state])
        return action_value

