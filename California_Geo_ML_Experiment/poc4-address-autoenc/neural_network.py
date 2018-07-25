import tensorflow as tf
import numpy as np

# hard-coded input and labels for demonstration
training_x = np.array([[1.], [2.],[3.],[4.],[5.]])
labels_training = np.array([[1,0],[0,1],[1,0],[0,1],[1,0]])

print('Input:\n' + str(training_x))
print('Training Output:\n' + str(labels_training))

# Hyperparameters
num_epochs = 100000
learning_rate = 0.001
HIDDEN = 20

# scan data
INPUT_SAMPLES = len(training_x)
INPUT_VARS = len(training_x[0])
OUTPUT_CLASSES = len(labels_training[0])
OUTPUT_SAMPLES = len(labels_training)
print("Input samples = " + str(INPUT_SAMPLES) + ", OUTPUT_CLASSES=" + str(OUTPUT_CLASSES) + ", OUTPUT_SAMPLES=" + str(OUTPUT_SAMPLES))

# setup the Neural Network
X = tf.placeholder(tf.float32, shape=[None, INPUT_VARS])
Y = tf.placeholder(tf.float32, shape=[None, OUTPUT_CLASSES])
parameters = {
    'W1': tf.Variable(tf.random_normal([INPUT_VARS, HIDDEN])),
    'b1': tf.Variable(tf.random_normal([HIDDEN])),
    'W2': tf.Variable(tf.random_normal([HIDDEN, OUTPUT_CLASSES])),
    'b2': tf.Variable(tf.random_normal([OUTPUT_CLASSES]))
}

print('W1: ' + str(parameters['W1']))
print('b1: ' + str(parameters['b1']))
print('X: ' + str(X))
print('W2: ' + str(parameters['W2']))
print('b2: ' + str(parameters['b2']))
print('Y: ' + str(Y))

Z1 = tf.add(tf.matmul(X, parameters['W1']), parameters['b1'])
A2 = tf.nn.relu(Z1)
Z2 = tf.add(tf.matmul(A2, parameters['W2']), parameters['b2']) 
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Z2,  labels=Y))

optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(num_epochs):
        _ , c = sess.run([optimizer, cost], feed_dict={X: training_x, Y: labels_training}) 
        if c <= 0.0005:
            break
        if epoch % 200 == 0:
            print ("Cost after epoch %i: %f" % (epoch, c))

    # Test predictions by computing the output using training set as input
    output = sess.run(Z2, feed_dict={X: training_x})
    print(np.array2string(output, precision=3))
    