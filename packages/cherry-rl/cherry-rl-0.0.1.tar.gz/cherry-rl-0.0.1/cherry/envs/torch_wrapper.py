#!/usr/bin/env python3

import numpy as np
import torch as th

from gym import Wrapper
from gym.spaces import Discrete


class Torch(Wrapper):

    """
    This wrapper converts
        * actions from Tensors to numpy,
        * states from lists/numpy to Tensors.

    Example:
        action = Categorical(Tensor([1, 2, 3])).sample()
        env.step(action)
    """

    def __init__(self, env):
        super(Torch, self).__init__(env)

    def _convert_state(self, state):
        if isinstance(state, (float, int)):
            state = np.array([state])
        return th.from_numpy(state).float().unsqueeze(0)

    def step(self, action):
        if isinstance(action, th.Tensor):
            action = action.view(-1).numpy()
        if isinstance(self.env.action_space, Discrete):
            action = action[0]
        state, reward, done, info = self.env.step(action)
        state = self._convert_state(state)
        return state, reward, done, info

    def reset(self, *args, **kwargs):
        state = self.env.reset(*args, **kwargs)
        state = self._convert_state(state)
        return state

    def seed(self, *args, **kwargs):
        return self.env.seed(*args, **kwargs)
