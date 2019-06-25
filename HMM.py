import sklearn
from hmmlearn import hmm
import numpy as np
N = 2
M = 3
obserstate = ['哭','没精神','找妈妈']#可观测状态
state = ['吃','睡']#隐藏状态
start_probability = np.array([0.3, 0.7])#初始化概率
transition_probability_matrix = np.array([
  [0.1, 0.9],
  [0.8, 0.2]
])#转移概率矩阵
emission_probability_matrix = np.array([
  [0.7, 0.1, 0.2],
  [0.3, 0.5, 0.2]
])#生成概率矩阵
#生成hmm模型
model = hmm.MultinomialHMM(n_components=N)
model.startprob_= start_probability
model.transmat_ = transition_probability_matrix
model.emissionprob_ = emission_probability_matrix
#可观测序列哭 -> 没精神 –>找妈妈
baby_Actions = np.array([[0,1,2]]).T
actions = ''
for i in range(len(baby_Actions)):
    if(not i == 0):
        actions = actions + '->' + obserstate[baby_Actions[i][0]]
    else:
        actions = actions +  obserstate[baby_Actions[i][0]]
#已知整个模型，估算概率
score = model.score(baby_Actions, lengths=None)
print(actions + '的概率为:',round(np.exp(score),6))
#已知整个模型，寻找最可能的状态
tuple = model.decode(baby_Actions, algorithm="viterbi")
actions_order = tuple[1]
possible_actions = ''
for i in range(len(actions_order)):
    index = actions_order[i]
    if (not i == 0):
        possible_actions = possible_actions + '->' + state[index]
    else:
        possible_actions = possible_actions + state[index]
print('最可能的状态为:',possible_actions)