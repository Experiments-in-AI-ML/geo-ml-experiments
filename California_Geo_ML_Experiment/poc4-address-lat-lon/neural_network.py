import tensorflow as tf
import numpy as np
# Example: 3 Layers Neutral Network (Input -> 1 Hidden Layer -> Output)
# Input Layer: 5 units, Hidden Layer: 3 units , Output Layer: 1 unit

# Hyperparameters
num_epochs = 1000 # Iteration for gradient descent
learning_rate = 0.001

# Define input and labels
training_x = np.array([[1., 2., 4., 6., 8.], [1., 4., 2., 3., 5.]]).T # 2 examples of inputs as training set.
labels_training = np.array([[1,0,0,0],[1,0,0,0]]).T # Labels in value of 1 and 0 for corresponding traning examples
print(labels_training)
# The input and output needs to be same type, as Tensorflow highly restrict the data type to be symettric
# for computation. Moreover, value for weights and biases need to be floating decimals due to gradient descent. 
# Which required, input and output value to inherit a floating decimal value. However, input value can be created
# as floating whole number to mimic integer value, and output can be rounded to integers

X = tf.placeholder(tf.float32, shape=[5,None])
Y = tf.placeholder(tf.float32, shape=[4, None])

# Initiate parameters for weights and biases.
parameters = {
    'W1': tf.Variable(np.random.randn(3,5), dtype=tf.float32),
    'b1': tf.Variable(np.zeros([3,1]), dtype=tf.float32),
    'W2': tf.Variable(np.random.randn(4,3), dtype=tf.float32),
    'b2': tf.Variable(np.zeros([4,1]), dtype=tf.float32)
}

# Forward propagation, ReLU as activation function (X -> Z1 -> ReLU(Z1) -> A2 -> Z2 -> Sigmoid(Z2) -> Output)
Z1 = tf.add(tf.matmul(parameters['W1'], X), parameters['b1']) # W1*X + b
A2 = tf.nn.relu(Z1) # ReLU - max(0,Z1)
Z2 = tf.add(tf.matmul(parameters['W2'], A2), parameters['b2']) 

# Compute sigmoid activation and calculate cross entropy (Input: Z2, not the sigmoid output)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=Z2,  labels=Y)) 
# Initiate optimizer. (gradient descent method used in backpropagation, in this case is Adam)
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initial all variables to be ready for computation
init = tf.global_variables_initializer()
# Tensorflow computation required tf.Session() to run certain command, and here "with ... as ..." is used for
# convinient purpose of closing the session after calling it.
with tf.Session() as sess:
    sess.run(init)
    for epoch in range(num_epochs):
        # Run tensorflow session to execute the forward-prop, then perform backprop, lastly then Adam gradient descent
        # Gradients are automatically calculated and it's the output for optimizer, (nullified by '_'), and c is the 
        # output for cost. 
        _ , c = sess.run([optimizer, cost], feed_dict={X: training_x, Y: labels_training}) 

        # Print the cost every epoch
        if epoch % 200 == 0:
            print ("Cost after epoch %i: %f" % (epoch, c))
    # Test predictions again by computing the output using training set as input again
    print(sess.run(tf.sigmoid(Z2), feed_dict={X: training_x})) # Raw output
    print(sess.run(tf.round(tf.sigmoid(Z2)), feed_dict={X: training_x})) # Rounded output   
    