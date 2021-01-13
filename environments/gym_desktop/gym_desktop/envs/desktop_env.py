import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_desktop.envs.actions.actionMap import actions
from gym_desktop.envs.actions.main import key_stroke, mouse_action, key_release

import numpy as np
import cv2
from gym_desktop.envs.CaptureStream import CaptureVideoStream
import pickle

import time
import faulthandler
from random import randint

faulthandler.enable()

# Goal
goal = np.array({})
with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)


class DesktopEnv(gym.Env):
    """
    Desktop Gym Environment

        Description:
        A Desktop GUI is rendered and the agent is given a task to complete. The agent submits states
        it believes to solve the task to a validation function. The validation function returns the distance
        the submitted state is from the goal state. This distance be expressed as a reward.

        Source:

        Observation:
        Type: Box(n)
        Size of window

        Actions:
        Type: Discrete(197) or [0-196]
        Mouse movements, button presses and key strokes.

        Rewards:
        action  1
        statechange  delta(currentstate, laststate) ...with decay?
        distance from state
        [energyuse]

        Starting State:
        reload desktop GUI
        center mouse
        release all keys

        Episode Termination:
            time limit - 1000 seconds 
            step limit - 100 steps

        Solved Requirements:
        Considered solved when the given state returns 0 (goal = state) when passes to the validation function.
    """
    metadata = {'render.modes': ['human', "rgb_array", "state_pixels"]}

    def __init__(self, debug=False, show=False, human=False, timelimit=1000, steplimit=100):
        self.camera = CaptureVideoStream(src=0, width=1920, height=1080).start()
        self.state_space = self.camera.read().shape
        self.observation_space = spaces.Box(
            low=0, high=255, shape=self.state_space, dtype=np.uint8
        )
        self.action_space = spaces.Discrete(197)
        self.debug = debug
        self.show = show
        self.step_limit = steplimit
        self.time_limit = timelimit

        self.human = human

    def step(self, action=None):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg
        self.last_time = time.time()
        frame = self.camera.read()
        self.state = frame
        done = False
        # Rewards
        action_reward = 1
        # distance (weighted pixels) from goal state, if 0 state equals goal
        if self.debug is False:
            goal_reward = (np.sum(goal, dtype='int64') - np.sum(self.state, dtype='int64'))
        else :
            goal_reward = 1

        step_reward = action_reward + goal_reward

        if self.human is True:
            # if action > 0:
            #     print('Human Action: ', action)
            pass
        else:
            # Actions:
            if action == 0:
                pass
            elif isinstance(actions[action], list):
                # Key Actions
                if self.debug is False:
                    key_stroke(actions[action])
                else:
                    print('KeyEvent:', actions[action])
                    pass

            elif isinstance(actions[action], int):
                # Mouse Actions
                if self.debug is False:
                    if action < 42:
                        mouse_action(0, actions[action], 0, 0)  # delta_x
                    elif action > 41 and action < 83:
                        mouse_action(0, 0, actions[action], 0)  # delta_y
                    elif action == 83:
                        mouse_action(actions[action], 0, 0, 0)  # btn_1
                    elif action == 84:
                        mouse_action(actions[action], 0, 0, 0)  # btn_2
                    elif action == 85:
                        mouse_action(actions[action], 0, 0, 0)  # btn_3
                    elif action == 86:
                        mouse_action(0, 0, 0, 0)  # none
                    elif action == 87:
                        mouse_action(0, 0, 0, actions[action])  # whl_dwn
                    elif action == 88:
                        mouse_action(0, 0, 0, actions[action])  # whl_none
                    elif action == 89:
                        mouse_action(0, 0, 0, actions[action])  # whl_up
                else:
                    print('MouseEvent: ', actions[action])
                    pass
            else:
                if self.debug is True:
                    print('NullEvent')
                pass
        
        
        self.step_count += 1
        if self.step_limit > 0 and self.step_count >= self.step_limit:
            print("Ending, step limit reached: ", self.step_count)
            done = True

        if self.time_limit > 0:
            runtime = self.last_time - self.start_time
            if runtime > self.time_limit:
                print("Ending, time limit reached: ", runtime)
                done = True

        return self.state, step_reward, done, {}

    def reset(self):
        self.step_count = 0
        self.start_time = time.time()
        self.last_time = self.start_time

        frame = self.camera.read()
        self.state = frame

        # TODO: relative mouse reset...
        # TODO: clear clipboard
        # TODO: release any keys
        return self.state

    def render(self, mode='human'):
        if self.state is None:
            print('Unable to render.')
            return None
        if self.debug is True:
            try:
                print("fps: {}".format(1 / (time.time() - self.last_time)))
            except ZeroDivisionError:
                pass
        if self.show is True:
            cv2.imshow("Frame", self.state)
            cv2.waitKey(1)
        return self.state

    def close(self):
        self.camera.stop()
        cv2.destroyAllWindows()
