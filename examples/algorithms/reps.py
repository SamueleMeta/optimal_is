"""Working example of REPS."""
import numpy as np
import torch

from rllib.agent import REPSAgent
from rllib.environment import GymEnvironment
from rllib.util.training.agent_training import evaluate_agent, train_agent

ETA = 1.0
NUM_EPISODES = 10000

GAMMA = 1
SEED = 0
ENVIRONMENT = "Pendulum-v0"
MAX_STEPS = 200

torch.manual_seed(SEED)
np.random.seed(SEED)

environment = GymEnvironment(ENVIRONMENT, SEED)

agent = REPSAgent.default(environment, epsilon=ETA, regularization=True, gamma=GAMMA)
train_agent(agent, environment, num_episodes=NUM_EPISODES, max_steps=MAX_STEPS + 1, plot_flag=False, print_frequency=10)
evaluate_agent(agent, environment, num_episodes=1, max_steps=MAX_STEPS + 1)
