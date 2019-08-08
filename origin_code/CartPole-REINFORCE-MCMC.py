import tensorflow as tf
import gym
import numpy as np
from gym import wrappers
# GLOBAL SETTINGS
RNG_SEED = 8
ENVIRONMENT = "CartPole-v0"
# ENVIRONMENT = "CartPole-v1"
MAX_EPISODES = 1000
HIDDEN_LAYER = True
HIDDEN_SIZE = 6
DISPLAY_WEIGHTS = False  # Help debug weight update
RENDER = False  # Render the generation representative
gamma = 0.99  # Discount per step
alpha = 0.02205  # Learning rate
# Upload to OpenAI
# UPLOAD = False
# EPISODE_INTERVAL = 50  # Generate a video at this interval
# SESSION_FOLDER = "/tmp/CartPole-experiment-1"
# API_KEY = ""
SUCCESS_THRESHOLD = 195
# SUCCESS_THRESHOLD = 475
CONSECUTIVE_TARGET = 100
def record_interval(n):
   global EPISODE_INTERVAL
   return n % EPISODE_INTERVAL == 0
env = gym.make(ENVIRONMENT)
# if UPLOAD:
#     env = wrappers.Monitor(env, SESSION_FOLDER, video_callable=record_interval)
env.seed(RNG_SEED)
np.random.seed(RNG_SEED)
tf.set_random_seed(RNG_SEED)
input_size = env.observation_space.shape[0]
env._max_episode_steps = 20001 #최대 유지 횟수
try:
   output_size = env.action_space.n # 수정
except AttributeError:
   output_size = env.action_space.n
# Tensorflow network setup
x = tf.placeholder(tf.float32, shape=(None, input_size))
y = tf.placeholder(tf.float32, shape=(None, 1))
expected_returns = tf.placeholder(tf.float32, shape=(None, 1))
w_init = tf.contrib.layers.xavier_initializer()
if HIDDEN_LAYER:
   hidden_W = tf.get_variable("W1", shape=[input_size, HIDDEN_SIZE], initializer=w_init) #히든사이즈 조정해 보자
   hidden_B = tf.Variable(tf.zeros(HIDDEN_SIZE))
   dist_W = tf.get_variable("W2", shape=[HIDDEN_SIZE, output_size], initializer=w_init)
   dist_B = tf.Variable(tf.zeros(output_size))
   hidden = tf.nn.elu(tf.matmul(x, hidden_W) + hidden_B) # input(4)이 hidden size만큼 펼쳐졌다가 다시 output size(2)만큼 줄어들음
   #지수 선형 유닛(ELU, Exponential Linear Unit) 함수는 softplus 함수와 비슷하지만 하부 점근선이 -1입니다.
   #x<0일 때는 exp(x)+1이고, 그외에는 x입니다.
   dist = tf.tanh(tf.matmul(hidden, dist_W) + dist_B) # hidden - [input, hidden], dist_w - [hidden, output] --> 즉 1행 2열의 데이터가 나옴
else:
   dist_W = tf.get_variable("W1", shape=[input_size, output_size], initializer=w_init)
   dist_B = tf.Variable(tf.zeros(output_size))
   dist = tf.tanh(tf.matmul(x, dist_W) + dist_B)
dist_soft = tf.nn.log_softmax(dist)
dist_in = tf.matmul(dist_soft, tf.Variable([[1.], [0.]])) # <tf.Variable 'Variable_3:0' shape=(2, 1) dtype=float32_ref>
#1행 2열의 dist_soft에 2행 1열의 Variable([[1.], [0.]]) 을 곱함 --> 하나의 값이 나올듯.. 이 값은 dist_in의 1행 1열의 데이터
#print(54321, tf.Variable([[1.], [0.]]))
print(135, dist_in)
pi = tf.contrib.distributions.Bernoulli(dist_in) #하나의 값을 베르누이 분포에 넣음
pi_sample = pi.sample()
print(pi_sample)

log_pi = pi.log_prob(y) # y값에 베르누이 분포의 log_prob취해 log_pi 생성
optimizer = tf.train.RMSPropOptimizer(alpha) #따라서 RMSProp에서는 일정한 학습 속도를 사용하지 않습니다. 대신에 “최근의 그라디언트의 크기의 연속 평균”
train = optimizer.minimize(-1.0 * expected_returns * log_pi)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
def run_episode(environment, render=False):
   raw_reward = 0
   discounted_reward = 0
   cumulative_reward = []
   discount = 1.0
   states = []
   actions = []
   obs = environment.reset() # 우리는 하드웨어의 리셋을 해야할 듯..
   done = False
   while not done:
       states.append(obs) #상태 누적 (리스트로)
       cumulative_reward.append(discounted_reward) #보상 누적
       if render: #render 가 TRUE일 때
           obs.render()
       action = sess.run(pi_sample, feed_dict={x: [obs]})[0] # pi_sample의 의미??
       actions.append(action) #액션 누적
       obs, reward, done, info = env.step(action[0]) #real-world에서 받아와야 할 듯
       raw_reward += reward # 보상의 합 누적하여 저장
       if reward > 0: # 보상이 0이면 그냥 더하고, 양수이면 디스카운트 후 더함
           discounted_reward += reward * discount
       else:
           discounted_reward += reward
       discount *= gamma # 감마가 0.99이기 때문에 디스카운트는 점점 작아짐. --> 초기학습률이 나중보다 높음. 나중에는 안정성이 더해질듯
   return raw_reward, discounted_reward, cumulative_reward, states, actions # 보상누적합raw, 보상누적합disc, 보상리스트, 상태리스트, 액션리스트
   #에피소드 끝(드론이 땅에 충돌 등)에 해당 상태에서 어떤 액션을 해서 어떤 리워드를 받았는지 저장된 리스트를 리턴
def display_weights(session):
   global HIDDEN_LAYER
   if HIDDEN_LAYER:
       w1 = session.run(hidden_W)
       b1 = session.run(hidden_B)
       w2 = session.run(dist_W)
       b2 = session.run(dist_B)
       print(w1, b1, w2, b2)
   else:
       w1 = session.run(dist_W)
       b1 = session.run(dist_B)
       print(w1, b1)
returns = []
for ep in range(MAX_EPISODES): #MAX_EPISODES 수 만큼 진행
   raw_G, discounted_G, cumulative_G, ep_states, ep_actions = run_episode(env, RENDER and not UPLOAD)
   expected_R = np.transpose([discounted_G - np.array(cumulative_G)])
#     print(1, discounted_G) # 보상 누적합 (discounter)
#     print(2, np.array(cumulative_G)) # 보상 리스트
#     print(3, [discounted_G - np.array(cumulative_G)]) # 누적합에서 각각의 보상을 뺌.
#     print(4, np.transpose([discounted_G - np.array(cumulative_G)])) #이를 transpose --> 가로축이 세로축으로 변경
   sess.run(train, feed_dict={x: ep_states, y: ep_actions, expected_returns: expected_R}) #상태 리스트, 액션 리스트, 계산된 보상 리스트를 feed_dict의 인자로 사용
   #초기 값일수록 더 큰 보상을 바라는 방향으로 학습..
   #초기선택이 중요한듯??
   #우리 드론 학습에 적용할 때 효과적일듯
   if DISPLAY_WEIGHTS:
       display_weights(sess)
   returns.append(raw_G) # raw_reward의 합들을 returns라는 배열에 저장
   returns = returns[-CONSECUTIVE_TARGET:] # returns 리스트의 뒤의 100개 ( CONSECUTIVE_TARGET == 100) 만 사용
   mean_returns = np.mean(returns) # 그렇게 만들어짐 returns를 평균냄 --> 뒤의 100개 리턴값들의 평균값
   msg = "Episode: {}, Return: {}, Last {} returns mean: {}"
   msg = msg.format(ep, raw_G, CONSECUTIVE_TARGET, mean_returns)
   print(msg)
env.close()
# if UPLOAD:
#     gym.upload(SESSION_FOLDER, api_key=API_KEY)
Policy Gradient - Monte Carlo  카트 폴 예제입니다
