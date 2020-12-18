from gym.envs.registration import register

register(
    id='Multi-v0',
    entry_point='gym_multi.envs:MultiEnv',
)