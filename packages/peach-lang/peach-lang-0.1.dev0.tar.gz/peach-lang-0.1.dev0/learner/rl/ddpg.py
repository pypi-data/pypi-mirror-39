from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess



class DDPGLearner:
    def __init__(self, name, observations, actions):
        self.name = name

        obs_s = observations
        act_s = actions

        actor = Sequential()
        actor.add(Flatten(input_shape=(1,) + (obs_s,)))
        actor.add(Dense(obs_s * 8))
        actor.add(Activation('elu'))
        actor.add(Dense(obs_s * 8))
        actor.add(Activation('elu'))
        actor.add(Dense(obs_s * 8))
        actor.add(Activation('elu'))
        actor.add(Dense(actions))
        actor.add(Activation('tanh'))
        #print(actor.summary())

        action_input = Input(shape=(act_s,), name='action_input')
        observation_input = Input(shape=(1,) + (obs_s,), name='observation_input')
        flattened_observation = Flatten()(observation_input)
        x = Concatenate()([action_input, flattened_observation])
        x = Dense((obs_s + act_s) * 8)(x)
        x = Activation('elu')(x)
        x = Dense((obs_s + act_s) * 8)(x)
        x = Activation('elu')(x)
        x = Dense((obs_s + act_s) * 8)(x)
        x = Activation('elu')(x)
        x = Dense(1)(x)
        x = Activation('linear')(x)
        critic = Model(inputs=[action_input, observation_input], outputs=x)
        #print(critic.summary())

        memory = SequentialMemory(limit=100000, window_length=1)
        random_process = OrnsteinUhlenbeckProcess(size=act_s, theta=.15, mu=0., sigma=.3)
        agent = DDPGAgent(nb_actions=act_s, actor=actor, critic=critic, critic_action_input=action_input,
                          memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                          random_process=random_process, gamma=.99, target_model_update=1e-3)
        agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])
        self.agent = agent



    def fit(self,env, nb_steps=1000):
        hist = self.agent.fit(env, nb_steps=nb_steps, visualize=False, verbose=2, nb_max_episode_steps=200,
                              log_interval=1000)
        return hist


    def save(self,path):
        self.agent.save_weights(path, overwrite=True)

    def load(self,path):
        self.agent.load_weights(path)

    def test(self,env,nb_episodes=100):
        hist = self.agent.test(env, nb_episodes=nb_episodes, visualize=True, verbose=2)
        return hist
