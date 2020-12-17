import gym
from gym import error, spaces, utils
from gym.utils import seeding
import time
import cv2
import mss
import numpy as np
import faulthandler
import gym_desktop.envs.actions as actions
from gym_desktop.envs.events import KeyEvent, PointerEvent, WaitEvent
import imutils
from imutils.video import WebcamVideoStream

faulthandler.enable()

# State Constants
STATE_W = 1920   
STATE_H = 1080

# Action Constants
keyMap = actions.keymaps.machineKeyMap.keys

def keycode(key):
    if key in keyMap:
        return keyMap[key]
    else:
        raise error.Error(
            'Not sure how to translate to keycode: {!r}'.format(key))

def relative_pos(pos, total):
    """
    pos - int : position of cursor
    total - int : total width or height
    """
    return min(1.0, max(0.0, pos / total))

class ActionSpace(gym.Space):
    """The space of Desktop actions.
    https://github.com/openai/universe/blob/master/universe/spaces/vnc_action_space.py

    You can submit a list of KeyEvents or PointerEvents. KeyEvents
    correspond to pressing or releasing a key. PointerEvents correspond
    to moving to a specific pixel, and setting the mouse buttons to some state
    (buttonmask is a bitmap corresponding to which buttons are down).

    Note that key releases work differently from click releases: keys
    are stateful and must be explicitly released, while the state of
    the mouse buttons is provided at each timestep, so you have to
    explicitly keep the mouse down.

    Attributes:
        keys (list<KeyEvent>): The allowed key presses
        buttonmasks (list<int>): The allowed buttonmasks (i.e. mouse presses)
        screen_shape (int, int): The X and Y dimensions of the screen

    """
    def __init__(self, keys=None, buttonmasks=None, screen_shape=(STATE_W, STATE_H)):
        self._np_random = None
        # TODO : document & consider removing extra mapping?
        self.keys = []
        if keys is None:
            keys = keyMap
            print('load keymap')
        for key in keys:
            self.keys.append(key)
        self._key_set = set(self.keys)

        self._wait = 0

        self.screen_shape = screen_shape
        if self.screen_shape is not None:
            self.buttonmasks = buttonmasks
            # self.buttonmasks = []
            # if buttonmasks is None:
            #     buttonmasks = range(256)
            # for buttonmask in buttonmasks:
            #     self.buttonmasks.append(buttonmask)
            # self._buttonmask_set = set(self.buttonmasks)

    def contains(self, action):
        if not isinstance(action, list):
            return False

        for a in action:
            if isinstance(a, int):
                # KeyEvent
                if a not in self._key_set:
                    return False
            elif isinstance(a, list):
                # PointerEvent
                # a[0] - int, buttonmask 
                # a[1] - int, x  
                # a[2] - int, y
                # a[3] - int, v_wheel
                # a[4] - int, h_wheel
                if self.screen_shape is None:
                    return False
                if a[1] < 0 or a[1] > self.screen_shape[0]:
                    return False
                elif a[2] < 0 or a[2] > self.screen_shape[1]:
                    return False
                elif a[0] not in self.buttonmasks:
                    return False
                # TODO scrollwheel?
            elif isinstance(a, dict):
                # WaitEvent
                if a['wait'] < self._wait:
                    return False
        return True

    def sample(self):
        # Both key and pointer allowed
        if self.screen_shape is not None:
            event_type = self.np_random.randint(2)
        else:
            event_type = 0

        if event_type == 0:
            # Let's press a key
            key = self.np_random.choice(self.keys)
            event = [key.item()]
        else:
            x = self.np_random.randint(self.screen_shape[0])
            y = self.np_random.randint(self.screen_shape[1])
            relative_x = relative_pos(x, self.screen_shape[0])
            relative_y = relative_pos(y, self.screen_shape[1])            
            buttonmask = self.np_random.choice(self.buttonmasks)
            event = [[buttonmask,x,y,0,0]]
            # event = []
        return event


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
        self.action_space = ActionSpace(buttonmasks=[0,1,2,4]) # [none, left, right, middle]
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
        step_reward = 1
    
        # Actions:
        for a in action:
            # print(str(a))
            if isinstance(a, dict):
                # TODO: move to next state but, wait x amount before taking next action...
                # time.sleep(a["wait"])
                if self.debug is False:
                    pass
                else:
                    print('WaitEvent:' ,str(a))
                    pass
                
            elif isinstance(a, int):
                # integers which represent key presses
                if self.debug is False:
                    actions.main.key_stroke(keyMap[a])
                else:
                    print('KeyEvent:' ,str(keyMap[a]))
                    pass
                    
            elif isinstance(a, list):
                # list which represent x,y coordinate with a buttonmask (clicks)
                if self.debug is False:
                    actions.main.mouse_action(a)
                else:
                    print('MouseEvent: ', str(a[1]), ',', str(a[2]))
                    pass

        self.step_count+= 1
        print(self.step_count)
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
            actions.main.key_release()
            actions.main.mouse_action([0,0,0,0,0])
        cv2.destroyAllWindows()
        if self.no_show is False:
            frame = self.camera.read()
            # TODO: optimize resizing, implment CaptureStream.py?
            self.state = imutils.resize(frame, width=STATE_W)
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
        if self.debug is False:
            actions.main.key_release()
            actions.main.mouse_action([0,0,0,0,0])
        self.camera.stop()
        cv2.destroyAllWindows()
