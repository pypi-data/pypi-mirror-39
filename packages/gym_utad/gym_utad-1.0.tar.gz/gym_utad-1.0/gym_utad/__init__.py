from gym.envs.registration import register

register(
    id='EasyMountainCarEnv-v0',
    entry_point='gym_utad.envs:EasyMountainCarEnv',
    max_episode_steps=200,
)