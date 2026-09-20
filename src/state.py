"""Built states and admissible irreversible investments."""
STATES = ((0, 0), (0, 1), (1, 0), (1, 1))


def actions(state):
    x_c, x_u = state
    return tuple((c, u) for c in range(2 - x_c) for u in range(2 - x_u))


def next_state(state, action):
    return max(state[0], action[0]), max(state[1], action[1])
