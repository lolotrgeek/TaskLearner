import copy
import logging

import gym
import numpy as np
from PIL import ImageColor
from gym import spaces
from gym.utils import seeding

logger = logging.getLogger(__name__)

class MultiAgentActionSpace(list):
    def __init__(self, agents_action_space):
        for x in agents_action_space:
            assert isinstance(x, gym.spaces.space.Space)

        super(MultiAgentActionSpace, self).__init__(agents_action_space)
        self._agents_action_space = agents_action_space

    def sample(self):
        """ samples action for each agent from uniform distribution"""
        return [agent_action_space.sample() for agent_action_space in self._agents_action_space]

class MultiAgentObservationSpace(list):
    def __init__(self, agents_observation_space):
        for x in agents_observation_space:
            assert isinstance(x, gym.spaces.space.Space)

        super().__init__(agents_observation_space)
        self._agents_observation_space = agents_observation_space

    def sample(self):
        """ samples observations for each agent from uniform distribution"""
        return [agent_observation_space.sample() for agent_observation_space in self._agents_observation_space]

    def contains(self, obs):
        """ contains observation """
        for space, ob in zip(self._agents_observation_space, obs):
            if not space.contains(ob):
                return False
        else:
            return True

class MultiEnv(gym.Env):
    """
    Baseline for Multi-agent Environment.
    Source:
    https://github.com/koulanurag/ma-gym/blob/master/ma_gym/envs/predator_prey/predator_prey.py
    """
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, n_agents=2,full_observable=False, penalty=-0.5, step_cost=-0.01, task_reward=5, max_steps=100):
        self.n_agents = n_agents
        self._max_steps = max_steps
        self._step_count = None
        self._penalty = penalty
        self._step_cost = step_cost
        self._task_reward = task_reward

        self.action_space = MultiAgentActionSpace([spaces.Discrete(2) for _ in range(self.n_agents)])
        self.agent_pos = {_: None for _ in range(self.n_agents)}

        self._agent_dones = [False for _ in range(self.n_agents)]
        self.viewer = None
        self.full_observable = full_observable

        self._total_episode_reward = None
        self.seed()

    def action_space_sample(self):
        return [agent_action_space.sample() for agent_action_space in self.action_space]

    def __init_full_obs(self):
        self._full_obs = {}
        for agent_i in range(self.n_agents):
            print('setting state for agent', agent_i)
            while True:
                self.agent_pos[agent_i] = [0]
                break
            self.__update_agent_view(agent_i)

        
    def get_agent_obs(self):
        _obs = []
        for agent_i in range(self.n_agents):
            _agent_i_obs = self.agent_pos[agent_i]
            _obs.append(_agent_i_obs)

        if self.full_observable:
            _obs = np.array(_obs).flatten().tolist()
            _obs = [_obs for _ in range(self.n_agents)]
        return _obs

    def reset(self):
        self._total_episode_reward = [0 for _ in range(self.n_agents)]
        self.agent_pos = {}

        self.__init_full_obs()
        self._step_count = 0
        self._agent_dones = [False for _ in range(self.n_agents)]

        return self.get_agent_obs()


    def __update_agent_pos(self, agent_i, action):
        curr_pos = copy.copy(self.agent_pos[agent_i])
        next_pos = None
        if action == 0: 
            next_pos = [curr_pos[0] + 1]
        elif action == 1:  # no-op
            pass
        else:
            raise Exception('Action Not found!')

        if next_pos is not None:
            self.agent_pos[agent_i] = next_pos
            self.__update_agent_view(agent_i)

    def __update_agent_view(self, agent_i):
        print("agent ", agent_i, " observation: ", self.agent_pos[agent_i])
        # TODO: add agents observation to full_observation?
        # self._full_obs[self.agent_pos[agent_i]] = [np.array({})]

    def step(self, agents_action):
        self._step_count += 1
        rewards = [self._step_cost for _ in range(self.n_agents)]

        for agent_i, action in enumerate(agents_action):
            print("agent ", agent_i, " action: ", action)
            if not (self._agent_dones[agent_i]):
                self.__update_agent_pos(agent_i, action)

        if (self._step_count >= self._max_steps):
            for i in range(self.n_agents):
                self._agent_dones[i] = True

        for i in range(self.n_agents):
            self._total_episode_reward[i] += rewards[i]

        return self.get_agent_obs(), rewards, self._agent_dones, {}


    def render(self, mode='human'):
        pass

    def seed(self, n=None):
        self.np_random, seed = seeding.np_random(n)
        return [seed]

    def close(self):
        pass

PRE_IDS = {
    'agent': 'A',
}