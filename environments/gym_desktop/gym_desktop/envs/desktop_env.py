import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_desktop.envs.actions.actionMap import actions
from gym_desktop.envs.actions.main import key_stroke, mouse_action, key_release

import numpy as np
import cv2
import imutils
from imutils.video import WebcamVideoStream
import pickle

import time
import faulthandler
from random import randint

faulthandler.enable()

# State Constants
STATE_W = 640
STATE_H = 480

# Action Constants
no_key = 0
no_mouse = [0, 0, 0, 0]

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

    def __init__(self, debug=False, show=False, timelimit=1000, steplimit=100):
        self.camera = WebcamVideoStream(src=0).start()
        self.state_space = self.camera.read().shape
        self.observation_space = spaces.Box(
            low=0, high=255, shape=self.state_space, dtype=np.uint8
        )
        self.action_space = spaces.Discrete(197)
        self.debug = debug
        self.show = show
        self.step_limit = steplimit
        self.time_limit = timelimit

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
            goal_reward = (np.sum(goal) - np.sum(self.state)) * -1
        else :
            goal_reward = 1

        step_reward = action_reward + goal_reward

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
                    mouse_action([0, actions[action], 0, 0])  # delta_x
                elif action > 41 and action < 83:
                    mouse_action([0, 0, actions[action], 0])  # delta_y
                elif action == 83:
                    mouse_action([actions[action], 0, 0, 0])  # btn_1
                elif action == 84:
                    mouse_action([actions[action], 0, 0, 0])  # btn_2
                elif action == 85:
                    mouse_action([actions[action], 0, 0, 0])  # btn_3
                elif action == 86:
                    mouse_action([0, 0, 0, 0])  # none
                elif action == 87:
                    mouse_action([0, 0, 0, actions[action]])  # whl_dwn
                elif action == 88:
                    mouse_action([0, 0, 0, actions[action]])  # whl_none
                elif action == 89:
                    mouse_action([0, 0, 0, actions[action]])  # whl_up
            else:
                print('MouseEvent: ', actions[action])
                pass
        else:
            if self.debug is not False:
                print('NullEvent')
            pass

        self.step_count += 1
        if self.step_count >= self.step_limit:
            print("Ending, step limit reached: ", self.step_count)
            done = True

        runtime = self.last_time - self.start_time
        if runtime > self.time_limit:
            print("Ending, time limit reached: ", runtime)
            done = True
        return self.state, step_reward, done, {}

    def reset(self):
        self.step_count = 0
        self.start_time = time.time()
        self.last_time = self.start_time

        if self.debug is False:
            mouse_action(no_mouse)
            key_release()

        cv2.destroyAllWindows()
        frame = self.camera.read()
        self.state = frame
        # TODO: clear clipboard
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
