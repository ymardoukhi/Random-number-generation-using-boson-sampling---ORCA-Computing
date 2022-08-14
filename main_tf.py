import argparse
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


def train(n, m, d, n_params, v):

    training_steps = int(1e4)

    arch = SFArchitecture(n, m, d, n_params, v)

    # opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
    opt = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.3)
    eng = sf.Engine(backend="tf", backend_options={"cutoff_dim": n+1})

    tf_theta_list = [ tf.Variable(var) for var in np.random.uniform(0, 2*np.pi, n_params)]
    # tf_theta_list = [ tf.Variable(np.pi/4) for _ in range(theta_num) ]
    args_dict = {}
    for i in range(n_params):
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
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, help='number of photos')
    parser.add_argument('m', type=int, help='number of modes')
    parser.add_argument('d', type=int, help='depth of the circuit')
    parser.add_argument('n_param', type=int, help='number of beam-spliters')
    parser.add_argument('v', type=int, help='version of the architecture')
    args = parser.parse_args()

    thetas = train(args.n, args.m, args.d, args.n_param, args.v)
    print("End")

main()