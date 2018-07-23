import tensorflow as tf
import numpy as np

# hard-coded input and labels for demonstration
training_x = np.array([[1.], [2.],[3.],[4.],[5.]])
labels_training = np.array([[1.],[4.],[9.],[16.],[25.]])

# Hyperparameters
num_epochs = 50000
learning_rate = 0.001
LAYERS = 3

# setup the Neural Network
INPUT = len(training_x)
OUTPUT = len(labels_training)
X = tf.placeholder(tf.float32, shape=[INPUT,None])
Y = tf.placeholder(tf.float32, shape=[OUTPUT, None])
parameters = {
    'W1': tf.Variable(np.random.randn(LAYERS,INPUT), dtype=tf.float32),
    'b1': tf.Variable(np.zeros([LAYERS,1]), dtype=tf.float32),
    'W2': tf.Variable(np.random.randn(OUTPUT,LAYERS), dtype=tf.float32),
    'b2': tf.Variable(np.zeros([OUTPUT,1]), dtype=tf.float32)
}

Z1 = tf.add(tf.matmul(parameters['W1'], X), parameters['b1']) # W1*X + b
#Z1 = tf.add(tf.matmul(X, parameters['W1']), parameters['b1'])

A2 = tf.nn.relu(Z1)

Z2 = tf.add(tf.matmul(parameters['W2'], A2), parameters['b2']) 
#Z2 = tf.add(tf.matmul(A2, parameters['W2'], A2), parameters['b2']) 

#cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Z2,  labels=Y))
#cost = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(Z2, A2))))
cost = tf.reduce_mean(tf.losses.mean_squared_error(labels = Y, predictions = Z2))
 
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

    # Test predictions again by computing the output using training set as input again
    output = sess.run(Z2, feed_dict={X: training_x})
    print(np.array2string(output, precision=3))
    