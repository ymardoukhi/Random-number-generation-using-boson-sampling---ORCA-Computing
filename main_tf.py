import numpy as np
import tensorflow as tf
import strawberryfields as sf
from strawberryfields import ops

    
def entropy(probabilities):
    probs = [np.abs(prob.numpy())**2 for prob in probabilities]
    return tf.convert_to_tensor(np.sum([-prob*np.log(prob) for prob in probs]))

def main():

    eng = sf.Engine(backend="tf", backend_options={"cutoff_dim": 4})
    boson_sampling = sf.Program(4)

    tf_phi_1, tf_phi_2, tf_phi_3, tf_phi_4, tf_phi_5 =\
        [tf.Variable(np.pi/2) for _ in range(5) ]
    tf_theta_1, tf_theta_2, tf_theta_3, tf_theta_4, tf_theta_5 =\
        [tf.Variable(np.pi/4) for _ in range(5) ]

    theta_1, theta_2, theta_3, theta_4, theta_5,\
        phi_1, phi_2, phi_3, phi_4, phi_5 = boson_sampling.params(
            "theta_1", "theta_2", "theta_3", "theta_4", "theta_5",
            "phi_1", "phi_2", "phi_3", "phi_4", "phi_5")

    with boson_sampling.context as q:

        ops.Fock(1) | q[0]
        ops.Fock(0) | q[1]
        ops.Fock(0) | q[2]
        ops.Fock(0) | q[3]

        ops.BSgate(theta_1, phi_1) | (q[0], q[1])
        ops.BSgate(theta_2, phi_2) | (q[2], q[3])

        ops.BSgate(theta_3, phi_3) | (q[1], q[2])

        ops.BSgate(theta_4, phi_4) | (q[0], q[1])
        ops.BSgate(theta_5, phi_5) | (q[2], q[3])

    def loss():
        if eng.run_progs:
            eng.reset()

        with tf.GradientTape() as tape:
            result = eng.run(
                boson_sampling,
                args={
                    "theta_1": tf_theta_1, "theta_2": tf_theta_2,
                    "theta_3": tf_theta_3, "theta_4": tf_theta_4,
                    "theta_5": tf_theta_5, "phi_1": tf_phi_1,
                    "phi_2": tf_phi_2, "phi_3": tf_phi_3,
                    "phi_4": tf_phi_4, "phi_5": tf_phi_5}
                )
            prob = result.state.all_fock_probs()
            ent = -tf.math.reduce_sum(
                tf.math.multiply(tf.abs(prob[prob != 0.0 + 0.0j])**2,
                tf.math.log(tf.abs(prob[prob != 0.0 + 0.0j])**2)))
            return -ent

    

    opt = tf.keras.optimizers.Adam(learning_rate=0.1)
    steps = 1000

    for step in range(steps):
        _ = opt.minimize(loss, [
            tf_theta_1, tf_theta_2, tf_theta_3, tf_theta_4, tf_theta_5,
            tf_phi_1, tf_phi_2, tf_phi_3, tf_phi_4, tf_phi_5])
        parameters_val = [
            tf_theta_1.numpy(), tf_theta_2.numpy(), tf_theta_3.numpy(), tf_theta_4.numpy(), tf_theta_5.numpy(),
            tf_phi_1.numpy(), tf_phi_2.numpy(), tf_phi_3.numpy(), tf_phi_4.numpy(), tf_phi_5.numpy()
        ]
        print("Probability at step {}: {}".format(step, parameters_val))
        print("Loss: {}".format(loss()))

main()