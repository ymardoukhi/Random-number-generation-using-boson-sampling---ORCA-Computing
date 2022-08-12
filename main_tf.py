from operator import mod
from statistics import mode
import numpy as np
import tensorflow as tf
import strawberryfields as sf
from src.Architecture import SFArchitecture

    
def entropy_tf(probabilities):
    ent = -tf.math.reduce_sum(
        tf.math.multiply(
            tf.abs(probabilities[probabilities != 0.0 + 0.0j])**2,
            tf.math.log(tf.abs(probabilities[probabilities != 0.0 + 0.0j])**2)
            )
        )
    return ent


def train():

    n_photos = 3
    modes = 4
    depth = 3
    ver = 0
    theta_num = 5
    training_steps = int(1e4)

    arch = SFArchitecture(n_photos, modes, depth, theta_num, ver)

    # opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
    opt = tf.keras.optimizers.SGD(learning_rate=0.001, momentum=0.5)
    eng = sf.Engine(backend="tf", backend_options={"cutoff_dim": n_photos+1})

    tf_theta_list = [ tf.Variable(var) for var in np.random.uniform(0, 2*np.pi, theta_num)]
    # tf_theta_list = [ tf.Variable(np.pi/4) for _ in range(theta_num) ]
    args_dict = {}
    for i in range(theta_num):
        args_dict["theta_{}".format(i)] = tf_theta_list[i]

    def loss():
        if eng.run_progs:
            eng.reset()

        result = eng.run(arch.prog, args=args_dict)
        prob = result.state.all_fock_probs()
        ent = entropy_tf(prob)
        return -ent

    prev_loss = 0.0
    thresh = 1e-7
    for step in range(training_steps):
        _ = opt.minimize(loss, tf_theta_list)
        cur_loss = loss()
        parameters_val = [ tf_theta.numpy() for tf_theta in tf_theta_list]
        print("Thetas at step {}: {}".format(step, parameters_val))
        print("Entropy: {}".format(cur_loss))
        if abs(cur_loss - prev_loss) < thresh or np.nan in parameters_val:
            return parameters_val
        else:
            prev_loss = cur_loss

def main():
    thetas = train()
    print("End")

main()