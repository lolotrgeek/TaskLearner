import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import cv2
import mss
import numpy as np
import faulthandler
from gym_desktop.envs.actions import actionMap
import imutils
from imutils.video import WebcamVideoStream
from random import randint
import pickle

faulthandler.enable()

# State Constants
STATE_W = 1920   
STATE_H = 1080

# Action Constants
actions = actionMap.actions
no_key=0
no_mouse=[0,0,0,0]

# Goal
goal = np.array({})
with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)


class DesktopEnv(gym.Env):
    """
    Description:
      A Desktop GUI is rendered and the agent is given a task to complete. The agent submits states
      it believes to solve the task to a validation function. The validation function returns a boolean,
      true when the task is complete.
    
    Source:

    Observation:
      Type: Box(n)
      Size of window

    Actions:
      Type: Discrete(126)
      String   Action
      0x01     hex keycode
      ...

    Rewards:
      action  .01
      statechange  delta(currentstate, laststate) ...with decay?
      failure = -.01
      [energyuse]


    Starting State:
      reload chromium at fullscreen
      center mouse
      release all keys

    Episode Termination:
      reward = -100
      Episode length is greater than 200 seconds.


    Solved Requirements:
      Considered solved when the given state returns true when passes to the validation function.
    """

    metadata = {'render.modes': ['human', "rgb_array", "state_pixels"]}

    # "rgb_array" returns "numpy.ndarray"

    def __init__(self):
        self.camera = WebcamVideoStream(src=0).start()
        self.action_space = spaces.Discrete([1156])
        self.observation_space = spaces.Box(
            low=0, high=255, shape=(STATE_H, STATE_W, 3), dtype=np.uint8
        )

    def step(self, action=None):
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg
        self.last_time = time.time()
        if self.no_show is False:
            frame = self.camera.read()
            # self.state = imutils.resize(frame, width=STATE_W)
            self.state = frame
        else:
            self.state=np.array({})    

        done = False
        # Rewards
        action_reward = 1
        # distance (weighted pixels) from goal state, if 0 state equals goal
        goal_reward = (np.sum(goal) - np.sum(self.state)) * -1
        step_reward = action_reward + goal_reward

        # Actions:
        
        print(str(action))
        if isinstance(actions[action], list):
            # integers which represent key presses
            if self.debug is False:
                actions.main.key_stroke(actions[action])
            else:
                print('KeyEvent:' ,str(actions[action]))
                pass
                
        elif isinstance(actions[action], int):
            # list which represent x,y coordinate with a buttonmask (clicks)
            if self.debug is False:
                if action < 513:
                    actions.main.mouse_action([0, action, 0, 0]) # delta_x
                elif action > 513 and action < 1025:
                    actions.main.mouse_action([0, 0, action, 0]) # delta_y
                elif action == 1025:
                    actions.main.mouse_action([action, 0, 0, 0]) # btn_1
                elif action == 1026:
                    actions.main.mouse_action([action, 0, 0, 0]) # btn_2
                elif action == 1027:
                    actions.main.mouse_action([action, 0, 0, 0]) # btn_3
                elif action == 1028:
                    actions.main.mouse_action([0, 0, 0, 0]) # none
                elif action == 1029:
                    actions.main.mouse_action([0, 0, 0, action]) # whl_dwn
                elif action == 1030:
                    actions.main.mouse_action([0, 0, 0, action]) # whl_none
                elif action == 1031:
                    actions.main.mouse_action([0, 0, 0, action]) # whl_up                                                                                                                                           
            else:
                print('MouseEvent: ', str(action[1]), ',', str(action[2]))
                pass
        else: 
            if self.debug is not False:
                print('NullEvent')
            pass

        self.step_count+= 1
        if self.step_count >= self.step_limit:
            print("Ending, step limit reached: ", self.step_count)
            done = True

        runtime = self.last_time - self.start_time
        if runtime > self.time_limit:
            print("Ending, time limit reached: ", runtime)
            done = True
        return self.state, step_reward, done, {}

    def reset(self, timelimit=1000, steplimit=100, debug=False, noShow=False):
        """
        timelimit - int: seconds

        steplimit - int: number of steps
        """
        self.debug=debug
        self.no_show=noShow

        self.step_count=0
        self.step_limit = steplimit

        self.time_limit = timelimit
        self.start_time = time.time()
        self.last_time = self.start_time

        if self.debug is False:
            actions.main.mouse_action(no_mouse)
            actions.main.key_release()
        cv2.destroyAllWindows()
        if self.no_show is False:
            frame = self.camera.read()
            # TODO: optimize resizing, implment CaptureStream.py?
            # self.state = imutils.resize(frame, width=STATE_W)
            self.state = frame
        else:
            self.state=np.array({})   
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
        if self.no_show is False:
            cv2.imshow("Frame", self.state)
            cv2.waitKey(1)
        return self.state

    def close(self):
        self.camera.stop()
        cv2.destroyAllWindows()
