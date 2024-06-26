import numpy as np
from env.game2048 import Game2048
from agent.dqn_agent import DQNAgent

EPISODES = 1000
BATCH_SIZE = 32


def train():
    env = Game2048()
    state_shape = (4, 4, 1)  # Updated input shape to match model input
    num_actions = 4  # Up, Down, Left, Right
    agent = DQNAgent(state_shape, num_actions)

    for e in range(EPISODES):
        state = env.reset().astype("float32")  # Convert to float32
        state = np.reshape(state, [1, 4, 4, 1])  # Updated reshape
        for time in range(500):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = next_state.astype("float32")  # Convert to float32
            next_state = np.reshape(next_state, [1, 4, 4, 1])  # Updated reshape
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                agent.update_target_model()
