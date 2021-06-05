"""
Implements the Tabular MDP environment(s) from Duan et al., 2016
- 'RL^2 : Fast Reinforcement Learning via Slow Reinforcement Learning'.
"""

import numpy as np


class MDPEnv:
    """
    Tabular MDP env with support for resettable MDP params (new meta-episode),
    in addition to the usual reset (new episode).
    """
    def __init__(self, num_states, num_actions, max_ep_length=10):
        self._num_states = num_states
        self._num_actions = num_actions
        self._reward_means = None
        self._reward_stddev = 1.0
        self._state_transition_probabilities = None
        self._state = None
        self._ep_steps_so_far = 0
        self._max_ep_length = max_ep_length
        self.new_mdp()

    def new_mdp(self):
        self._new_state_transition_probabilities()
        self._new_reward_means()
        self._state = 0

    def _new_reward_means(self):
        rsa_mus = np.random.normal(
            loc=1.0, scale=1.0, shape=(self._num_states, self._num_actions))
        self._reward_means = rsa_mus

    def _new_state_transition_probabilities(self):
        p_aijs = []
        for a in range(self._num_actions):
            dirichlet_samples = np.random.dirichlet(
                alpha=np.ones(self._num_states),
                size=(self._num_states,)
            )
            p_aijs.append(dirichlet_samples)

        self._state_transition_probabilities = np.stack(p_aijs, axis=0)

    def step(self, a_t):
        t = self._ep_steps_so_far + 1
        s_t = self._state
        r_t_mu = self._reward_means[s_t, a_t]
        r_t_sigma = self._reward_stddev
        r_t_noise = np.random.normal(loc=0.0, scale=1.0)[0]
        r_t = r_t_mu + r_t_sigma * r_t_noise
        s_tp1_probs = self._state_transition_probabilities[a_t, s_t]
        s_tp1 = np.random.choice(
            a=self._num_states, p=s_tp1_probs)[0]
        done_t = False if t < self._max_ep_length else True
        return s_tp1, r_t, done_t, {}

    def reset(self):
        self._ep_steps_so_far = 0
        self._state = 0
        return self._state