import gym
import gym_multi
from gym_multi.envs.monitor import Monitor
from pyinstrument import Profiler

# Spawn 2 agents that each performs random actions
# source: 
# https://github.com/koulanurag/ma-gym/blob/master/examples/random_agent.py

profiler = Profiler()
profiler.start()

if __name__ == '__main__':
    # Run Environment
    env = gym.make('Multi-v0')
    env = Monitor(env, directory='recordings/', force=True)
    env.n_agents = 2
    episodes = 10

    for episode in range(episodes):
        done_n = [False for _ in range(env.n_agents)]
        ep_reward = 0

        env.seed(episode)
        obs_n = env.reset()
        env.render()

        while not all(done_n):
            action_n = env.action_space.sample()
            obs_n, reward_n, done_n, info = env.step(action_n)
            ep_reward += sum(reward_n)
            env.render()

        print('Episode #{} Reward: {}'.format(episode, ep_reward))
    env.close()
    
profiler.stop()
print(profiler.output_text(unicode=True, color=True))