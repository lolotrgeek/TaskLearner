import gym
import cv2
from gym.wrappers import Monitor
import gym_desktop

# Takes no actions, simply observes the environment

env = gym.make('Desktop-v0')


max_ep = 10

for ep_cnt in range(max_ep):
    step_cnt = 0
    ep_reward = 0
    done = False
    state = env.reset()

    while not done:
        next_state, reward, done, _ = env.step()
        env.render()
        step_cnt += 1
        ep_reward += reward
        state = next_state
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            env.close()
            break
    print('Episode: {}, Step count: {}, Episode reward: {}'.format(ep_cnt, step_cnt, ep_reward))

env.close()