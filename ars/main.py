
if __name__ == '__main__':
    hp = Hp()
    np.random.seed(hp.seed)
    work_dir = mkdir('exp', 'brs')
    monitor_dir = mkdir(work_dir, 'monitor')
    env = gym.make(hp.env_name)
    # env = wrappers.Monitor(env, monitor_dir, force=True)
    num_inputs = env.observation_space.shape[0]
    num_outputs = env.action_space.shape[0]
    policy = Policy(num_inputs, num_outputs)
    normalizer = Normalizer(num_inputs)
    train(env, policy, normalizer, hp)

