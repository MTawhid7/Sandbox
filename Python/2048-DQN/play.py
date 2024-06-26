import numpy as np
from env.game2048 import Game2048
from agent.dqn_agent import DQNAgent


def play():
    env = Game2048()
    state_shape = (1, 4, 4)
    num_actions = 4  # Up, Down, Left, Right
    agent = DQNAgent(state_shape, num_actions)
    agent.load("data/model_weights.h5")

    state = env.reset()
    state = np.reshape(state, [1, 4, 4])
    while not env.is_game_over():
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = np.reshape(next_state, [1, 4, 4])
        state = next_state
        env.print_board(state)

    print("Game over! Final score:", np.max(state))


if __name__ == "__main__":
    play()
