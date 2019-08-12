import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical

#Hyperparameters
learning_rate = 0.0002
gamma         = 0.98

class Policy(nn.Module):
    def __init__(self):
        super(Policy, self).__init__()
        self.data = [] #list
        
        # model generate
        self.fc1 = nn.Linear(4, 128)   #input, output , fully connected
        self.fc2 = nn.Linear(128, 2)   #input, output,  fully connected
        self.optimizer = optim.Adam(self.parameters(), lr=learning_rate)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.softmax(self.fc2(x), dim=0)
        return x
    
    # ( reward, log pi ) tuple 형태로 append
    def put_data(self, item):
        self.data.append(item)
        
    def train_net(self):
        R = 0   # return
        for r, log_prob in self.data[::-1]:
            R = r + gamma * R     #거꾸로 본 리턴
            loss = -log_prob * R  # log pi * vt
            self.optimizer.zero_grad()   # optimizer 이전에 값 안남아있게 0으로 만듬
            loss.backward()   # back propagation, auto diff, 자동으로 gradient 가 자동으로 계산됨
            self.optimizer.step()   # grad 업데이트
        self.data = []

def main():
    env = gym.make('CartPole-v1')
    pi = Policy()
    avg_t = 0.0
    print_interval = 20
    
    for n_epi in range(10000):
        obs = env.reset()
        for t in range(501): # CartPole-v1 forced to terminates at 500 step.
            obs = torch.tensor(obs, dtype=torch.float)
            out = pi(obs)
            m = Categorical(out)
            a = m.sample() #action 하나를 뽑아줌
            obs, r, done, info = env.step(a.item()) #action이 tensor 이기 때문에 scalar 형태로 보냄
            pi.put_data((r,torch.log(out[a]))) # log pi 값 기록
            if done:
                break
        avg_t += t 
        pi.train_net() # 한 ep 만큼의 폴리시를 학습시켜라
        
        if n_epi%print_interval==0 and n_epi!=0:
            print("# of episode :{}, avg score : {}".format(n_epi, avg_t/print_interval))
            avg_t = 0.0
    env.close()
    
if __name__ == '__main__':
    main()