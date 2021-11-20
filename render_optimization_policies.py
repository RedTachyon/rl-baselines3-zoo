import os
from os.path import exists
import numpy as np
import supersuit as ss
from array2gif import write_gif
from pettingzoo.sisl import multiwalker_v7
from stable_baselines3 import PPO
import sumo_rl

env = sumo_rl.ingolstadt7()
env = ss.pad_observations_v0(env)
env = ss.pad_action_space_v0(env)

n_agents = 8

policies = os.listdir("./optimization_policies/")

for policy in policies:
    filepath = "./optimization_policies/" + policy + "/best_model"
    if not exists(filepath + '.zip'):
        continue
    print("Loading new policy ", filepath)
    model = PPO.load(filepath)

    obs_list = []
    i = 0
    env.reset()
    reward = 0

    while True:
        for agent in env.agent_iter():
            observation, _, done, reward = env.last()
            action = (model.predict(observation, deterministic=True)[0] if not done else None)
            reward += reward

            reward = reward / n_agents

            env.step(action)
            i += 1
            if i % (len(env.possible_agents) + 1) == 0:
                obs_list.append(
                    np.transpose(env.render(mode="rgb_array"), axes=(1, 0, 2))
                )

        break

    print("writing gif")
    write_gif(
        obs_list, "./optimization_gifs/" + policy + "_" + "reward" + ".gif", fps=50
    )
