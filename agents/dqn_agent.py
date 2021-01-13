import sys
from pyinstrument import Profiler

import gym
from gym.wrappers import Monitor
import gym_desktop

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.dqn import MlpPolicy

# Learn optimal policy with Q learning
# source: 
# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

profiler = Profiler()
profiler.start()

# Setup Environment
print('Envrionment Setup...')
env = gym.make('Desktop-v0', debug=False, show=True, steplimit=100)
outdir = '/tmp/random-agent-results'
env = Monitor(env, directory=outdir, force=True)
episodes = 10
# Setup Agent
print('Agent Setup...')
model = DQN(MlpPolicy, env, verbose=0, buffer_size=500)
print('Returning Trained Model...')
model.learn(total_timesteps=1000, log_interval=4)
print('Saving Trained Model...')
model.save("deepq_desktop")

del model # remove to demonstrate saving and loading
print('Loading Trained Model...')
model = DQN.load("deepq_desktop")

def unique_reward(last_state, current_state):
    # rewards a current state that is different from the last state
    return (np.sum(last_state) - np.sum(current_state))

if __name__ == '__main__':
    try: 
        print('Running Environment')
        last_state = None          
        # Run Environment
        for episode in range(episodes):
            print('Episode:' , episode)
            obs = env.reset()
            reward = 0
            done = False
            while True:
                if done is True:
                    break
                action, _states = model.predict(obs, deterministic=True)
                obs, reward, done, info = env.step(action)
                last_state = obs
                env.render()
            print('Reward:', reward)
    except ConnectionRefusedError:
        print('FAILED: Unable to Connect. Try running in debug mode.')
    except:
        print ("FAILED: Unexpected error:", sys.exc_info()[0])
        raise        
    finally:    
        env.close()
        profiler.stop()

print(profiler.output_text(unicode=True, color=True))