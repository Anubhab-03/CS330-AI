import numpy as np
import copy

def policy_eval(N, p, gamma, policy, trans_r):
    # Initialize the value function
    V = np.zeros(N + 1)

    # Iterate until convergence
    while True:
        delta = 0.0
        for i in range(1, N):
            state = i
            value = V[i]

            # Update the value based on the Bellman equation
            if i + policy[i] == N:
                V[i] = p * (2 * N + gamma * V[i + policy[i]]) + (1 - p) * (trans_r + gamma * V[i - policy[i]])
            else:
                V[i] = p * (trans_r + gamma * V[i + policy[i]]) + (1 - p) * (trans_r + gamma * V[i - policy[i]])

            # Update the change in values
            delta = max(delta, abs(value - V[i]))

        # Check for convergence
        if delta < 0.01:
            V[N] = 2 * N
            break

    return np.array(V)

def value_iteration(N, p, gamma, trans_r):
    # Initialize value function and actions
    V = np.zeros(N + 1)
    A = np.zeros(N + 1, dtype=int)
    V_new = np.zeros(N + 1)

    # Iterate until convergence
    while True:
        V_new = copy.copy(V)
        delta = 0.0

        for i in range(1, N):
            state = i
            value = V_new[i]

            # Find the action that maximizes the expected cumulative reward
            fl = True
            for actions in range(0, min(state, N - state) + 1):
                if i + actions == N:
                    new_v = p * (2 * N + gamma * V[i + actions]) + (1 - p) * (trans_r + gamma * V[i - actions])
                else:
                    new_v = p * (trans_r + gamma * V[i + actions]) + (1 - p) * (trans_r + gamma * V[i - actions])

                # Update value and action
                if fl:
                    V_new[i] = new_v
                    A[i] = actions
                    fl = not fl
                elif new_v > V_new[i]:
                    V_new[i] = new_v
                    A[i] = actions

            # Update the change in values
            delta = max(delta, abs(value - V_new[i]))

        # Check for convergence
        if delta < 0.001:
            V_new[N] = 2 * N
            break

        V = V_new

    return np.array(V_new), np.array(A)

def policy_iteration(N, p, gamma, trans_r):
    # Initialize the initial policy
    policy = np.ones(N + 1, dtype=int)
    policy[0] = 0
    policy[N] = 0

    # Perform policy evaluation and improvement until convergence
    V = policy_eval(N, p, gamma, policy, trans_r)
    while True:
        flag = True
        V = policy_eval(N, p, gamma, policy, trans_r)
        V[N] = 0

        for i in range(1, N):
            old_action = policy[i]

            # Find the action that maximizes the expected cumulative reward
            for actions in range(0, min(i, N - i) + 1):
                if i + actions == N:
                    new_v = p * (2 * N + gamma * V[i + actions]) + (1 - p) * (trans_r + gamma * V[i - actions])
                else:
                    new_v = p * (trans_r + gamma * V[i + actions]) + (1 - p) * (trans_r + gamma * V[i - actions])

                # Update value and policy
                if new_v > V[i]:
                    V[i] = new_v
                    policy[i] = actions

            # Check if the policy has changed
            if policy[i] != old_action:
                flag = False

        # Break if the policy does not change
        if flag:
            break

    V[N] = 2 * N

    return np.array(V), np.array(policy)

# Set parameters for the MDP problem
N = 10
p = 0.4
gamma = 0.9
transition_reward = -1

# Test the algorithms and print the results
v, A = value_iteration(N, p, gamma, transition_reward)
print("Optimal Policy (Value Iteration):", A)
print("Optimal Value Function (Value Iteration):", v)

v2, A2 = policy_iteration(N, p, gamma, transition_reward)
print("Optimal Policy (Policy Iteration):", A2)
print("Optimal Value Function (Policy Iteration):", v2)
