#!/usr/bin/env python
# coding: utf-8

import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

# import gym 
import gym
from snake import SnakeEnv

gym.register(id='Snake-v1', entry_point='snake:SnakeEnv')
env = gym.make('Snake-v1')

Q_table = np.zeros((SnakeEnv.GRID_WIDTH, SnakeEnv.GRID_HEIGHT, 4) + (env.action_space.n,))

def policy( state : Tuple ):
    """Choosing action based on epsilon-greedy policy"""
    return np.argmax(Q_table[state])

def new_Q_value( reward : float ,  new_state : tuple , discount_factor=1 ) -> float:
    """Temperal diffrence for updating Q-value of state-action pair"""
    future_optimal_value = np.max(Q_table[new_state])
    learned_value = reward + discount_factor * future_optimal_value
    return learned_value

def learning_rate(n : int , min_rate=1e-1 ) -> float  :
    """Decaying learning rate"""
    return max(min_rate, 0.999**(10*n))

def exploration_rate(n : int, min_rate=1e-6 ) -> float :
    """Decaying exploration rate"""
    return max(min_rate, 0.999**(50*n))

n_episodes = 150
total_rewards = []
avg_rewards = []
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
for e in range(n_episodes):
    
    # Siscretize state into buckets
    current_state, _ = env.reset()
    done = False
    total_reward = 0
    while done==False:
        
        # insert random action
        if np.random.random() < exploration_rate(e): 
            action = env.action_space.sample() # explore
        else:
            # policy action
            action = policy(current_state) # exploit
         
        # increment enviroment
        new_state, reward, done, _, info = env.step(action)

        if not done:
            total_reward += reward > 0
        
        # Update Q-Table
        lr = learning_rate(e)
        learnt_value = new_Q_value(reward , new_state)
        old_value = Q_table[current_state][action]
        Q_table[current_state][action] = (1-lr)*old_value + lr*learnt_value
        
        current_state = new_state
        
        # Render game
        env.render()

    #print("esp = %s, scores = %s" % (e, total_reward))
    total_rewards.append(total_reward)
    avg_rewards.append(np.average(total_rewards))
    ax1.cla()
    ax2.cla()
    ax1.set_xlabel('episode')
    ax1.plot(list(range(e+1)), total_rewards, 'g')
    ax1.set_ylabel('scores', color='g')
    ax2.plot(list(range(e+1)), avg_rewards, 'b')
    ax2.set_ylabel('avg scores', color='b')
    ax2.yaxis.set_label_position('right')
    plt.draw()
    plt.pause(0.01)

print('Done!')
plt.show()
