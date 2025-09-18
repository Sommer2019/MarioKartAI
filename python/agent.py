import torch
import torch.nn as nn
import torch.optim as optim
from config import STATE_DIM, ACTION_DIM, LR, BUFFER_SIZE

class Actor(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(STATE_DIM,128), nn.ReLU(), nn.Linear(128,ACTION_DIM), nn.Tanh())
    def forward(self,x):
        return self.fc(x)

class Critic(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(STATE_DIM,128), nn.ReLU(), nn.Linear(128,1))
    def forward(self,x):
        return self.fc(x)

class PPOAgent:
    def __init__(self):
        self.actor = Actor()
        self.critic = Critic()
        self.optimizer = optim.Adam(list(self.actor.parameters())+list(self.critic.parameters()),lr=LR)
        self.memory = []
    def select_action(self,state):
        state_tensor = torch.FloatTensor(state)
        action = self.actor(state_tensor).detach().numpy()
        action[1] = 1 if action[1]>0 else 0
        action[2] = 1 if action[2]>0 else 0
        return action
    def store_transition(self,state,action,reward):
        self.memory.append((state,action,reward))
        if len(self.memory)>BUFFER_SIZE:
            self.memory.pop(0)
    def train_if_ready(self):
        if len(self.memory)<BUFFER_SIZE: return
        states,actions,rewards = zip(*self.memory)
        states = torch.FloatTensor(states)
        actions = torch.FloatTensor(actions)
        rewards = torch.FloatTensor(rewards)
        values = self.critic(states).squeeze()
        advantage = rewards-values.detach()
        loss_actor = ((self.actor(states)-actions)**2*advantage.unsqueeze(1)).mean()
        loss_critic = advantage.pow(2).mean()
        loss = loss_actor+loss_critic
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.memory=[]
