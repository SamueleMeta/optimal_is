"""Working example of REPS."""
import numpy as np
import torch

from rllib.agent.off_policy.optimalIS_agent import OptimalISAgent
from rllib.agent.off_policy.reps_agent import REPSAgent
from rllib.environment.mdps import RandomMDP
from rllib.util.training.agent_training import train_agent

from rllib.policy import TabularPolicy
from rllib.value_function import TabularValueFunction

from rllib.algorithms.performance import evaluate_performance
from rllib.util.rollout import step_env
from rllib.util.training.utilities import Evaluate
from rllib.util.utilities import tensor_to_distribution

from rllib.algorithms.notebook import run_notebook

import matplotlib.pyplot as plt
from tqdm import tqdm

def rollout_episode(environment, agent, max_steps, render, gamma):
    """Rollout a full episode."""

    state = environment.reset()
    agent.set_goal(environment.goal)
    agent.start_episode()
    done = False
    time_step = 0

    ret = 0.
    agent.act(state)

    while not done:
        state = torch.tensor(state, dtype=torch.get_default_dtype(), device=agent.device)
        policy = agent.policy(state)
        pi = tensor_to_distribution(policy, **agent.policy.dist_params)
        action = pi.sample()  # agent.act(state)
        obs, state, done, info = step_env(
            environment=environment,
            state=state,
            action=action,
            action_scale=agent.policy.action_scale,
            pi=agent.pi,
            render=render,
        )

        ret += obs.reward * gamma ** time_step
        agent.observe(obs)
        # Log info.
        agent.logger.update(**info)

        time_step += 1
        if max_steps <= time_step:
            break

    agent.end_episode()

    return ret


def evaluate_agent(agent, environment, num_episodes, max_steps, gamma):
    rets = []
    for i in tqdm(range(num_episodes)):
        ret = rollout_episode(environment, agent, max_steps, False, gamma)
        rets.append(ret)

    print("Empirical performance: %s" % np.mean(rets))
    return np.mean(rets)

ETA = 1.0
NUM_EPISODES = 10000

GAMMA = 0.99
SEED = 0
MAX_STEPS = 1 / (1 - GAMMA)

torch.manual_seed(SEED)
np.random.seed(SEED)

environment = RandomMDP(num_states=5, num_actions=5)

#print(environment.transitions)

critic = TabularValueFunction.default(environment)
policy = TabularPolicy.default(environment)

#optimalIS_agent = OptimalISAgent.default(environment, epsilon=ETA, regularization=True, gamma=GAMMA, critic=critic, policy=policy)
reps_agent = REPSAgent.default(environment, epsilon=ETA, regularization=True, gamma=GAMMA, critic=critic, policy=policy)

'''
run_notebook(environment, policy, GAMMA, agent)

print('Before training...')
with Evaluate(agent):
    evaluate_agent(agent, environment, num_episodes=20, max_steps=MAX_STEPS + 1, gamma=GAMMA)
    evaluate_performance(environment, agent.policy, GAMMA, agent)
'''

#train_agent(optimalIS_agent, environment, num_episodes=NUM_EPISODES, max_steps=MAX_STEPS + 1, plot_flag=False, print_frequency=100)
train_agent(reps_agent, environment, num_episodes=NUM_EPISODES, max_steps=MAX_STEPS + 1, plot_flag=False, print_frequency=100)


print('After training...')
'''
with Evaluate(agent):
    empirical_performance = evaluate_agent(optimalIS_agent, environment, num_episodes=100, max_steps=MAX_STEPS + 1, gamma=GAMMA)
    with open("results.txt", "a") as file:
                file.write(f"empirical_performance: {empirical_performance}")
    evaluate_performance(environment, optimalIS_agent.policy, GAMMA, optimalIS_agent)

'''
with Evaluate(original_agent):
    empirical_performance = evaluate_agent(reps_agent, environment, num_episodes=100, max_steps=MAX_STEPS + 1, gamma=GAMMA)
    with open("results.txt", "a") as file:
                file.write(f"empirical_performance: {empirical_performance}")
    evaluate_performance(environment, reps_agent.policy, GAMMA, reps_agent)