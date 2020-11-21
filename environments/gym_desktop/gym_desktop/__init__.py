from gym.envs.registration import register

register(
    id='Desktop-v0',
    entry_point='gym_desktop.envs:DesktopEnv',
)