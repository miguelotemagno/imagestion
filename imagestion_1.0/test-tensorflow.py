import math
import tensorflow as tf
import time
import numpy as np

#http://stackoverflow.com/questions/33747596/problems-implementing-an-xor-gate-with-neural-nets-in-tensorflow
#http://stackoverflow.com/questions/33759623/tensorflow-how-to-restore-a-previously-saved-model-python
#https://www.tensorflow.org/versions/r0.9/tutorials/mnist/beginners/index.html
#https://www.tensorflow.org/versions/r0.9/get_started/index.html#introduction
#https://github.com/tensorflow/tensorflow/issues/1965   (fix problem: AttributeError: type object 'NewBase' has no attribute 'is_abstract')

## # Ubuntu/Linux 64-bit
## $ sudo apt-get install python-pip python-dev
## # Ubuntu/Linux 64-bit, CPU only, Python 2.7
## $ export TF_BINARY_URL=https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-0.9.0-cp27-none-linux_x86_64.whl

# HIDDEN_NODES = 10
#
# x = tf.placeholder(tf.float32, [None, 2])
# W_hidden = tf.Variable(tf.truncated_normal([2, HIDDEN_NODES], stddev=1./math.sqrt(2)))
# b_hidden = tf.Variable(tf.zeros([HIDDEN_NODES]))
# hidden = tf.nn.relu(tf.matmul(x, W_hidden) + b_hidden)
#
# W_logits = tf.Variable(tf.truncated_normal([HIDDEN_NODES, 2], stddev=1./math.sqrt(HIDDEN_NODES)))
# b_logits = tf.Variable(tf.zeros([2]))
# logits = tf.matmul(hidden, W_logits) + b_logits
#
# y = tf.nn.softmax(logits)
#
# y_input = tf.placeholder(tf.float32, [None, 2])
#
# cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits, y_input)
# loss = tf.reduce_mean(cross_entropy)
#
# train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
#
# init_op = tf.initialize_all_variables()
#
# sess = tf.Session()
# sess.run(init_op)
#
# xTrain = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# yTrain = np.array([[1,0], [0,1], [0,1], [1,0]])
#
# print xTrain
# print yTrain
#
# for i in xrange(500):
# 	_, loss_val = sess.run([train_op, loss], feed_dict={x: xTrain, y_input: yTrain})
#
# 	if i % 10 == 0:
# 		print "Step:", i, "Current loss:", loss_val
# 		for x_input in [[0, 0], [0, 1], [1, 0], [1, 1]]:
# 			result = sess.run(y, feed_dict={x: [x_input]})
# 			print "%s => %s" % (x_input, result)

######################################################################
#
# x_ = tf.placeholder(tf.float32, shape=[4,2], name="x-input")
# y_ = tf.placeholder(tf.float32, shape=[4,1], name="y-input")
#
# Theta1 = tf.Variable(tf.random_uniform([2,2], -1, 1), name="Theta1")
# Theta2 = tf.Variable(tf.random_uniform([2,1], -1, 1), name="Theta2")
#
# Bias1 = tf.Variable(tf.zeros([2]), name="Bias1")
# Bias2 = tf.Variable(tf.zeros([1]), name="Bias2")
#
# A2 = tf.sigmoid(tf.matmul(x_, Theta1) + Bias1)
# Hypothesis = tf.sigmoid(tf.matmul(A2, Theta2) + Bias2)
#
# cost = tf.reduce_mean(( (y_ * tf.log(Hypothesis)) +
#         ((1 - y_) * tf.log(1.0 - Hypothesis)) ) * -1)
#
# train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
#
# XOR_X = [[0,0],[0,1],[1,0],[1,1]]
# XOR_Y = [[0],[1],[1],[0]]
#
# init = tf.initialize_all_variables()
# sess = tf.Session()
# sess.run(init)
#
# for i in range(10000):
#     sess.run(train_step, feed_dict={x_: XOR_X, y_: XOR_Y})
#
# print('Epoch ', i)
# print('Hypothesis ', sess.run(Hypothesis, feed_dict={x_: XOR_X, y_: XOR_Y}))
# print('Theta1 ', sess.run(Theta1))
# print('Bias1 ', sess.run(Bias1))
# print('Theta2 ', sess.run(Theta2))
# print('Bias2 ', sess.run(Bias2))
# print('cost ', sess.run(cost, feed_dict={x_: XOR_X, y_: XOR_Y}))
#
########################################################################


X = tf.placeholder(tf.float32, shape=[4,2], name = 'X')
Y = tf.placeholder(tf.float32, shape=[4,1], name = 'Y')

W = tf.Variable(tf.truncated_normal([2,2]), name = "W")
w = tf.Variable(tf.truncated_normal([2,1]), name = "w")

c = tf.Variable(tf.zeros([4,2]), name = "c")
b = tf.Variable(tf.zeros([4,1]), name = "b")

with tf.name_scope("hidden_layer") as scope:
    h = tf.nn.relu(tf.add(tf.matmul(X, W),c))

with tf.name_scope("output") as scope:
    y_estimated = tf.sigmoid(tf.add(tf.matmul(h,w),b))

with tf.name_scope("loss") as scope:
    loss = tf.reduce_mean(tf.squared_difference(y_estimated, Y))

with tf.name_scope("train") as scope:
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

INPUT_XOR = [[0,0],[0,1],[1,0],[1,1]]
OUTPUT_XOR = [[0],[1],[1],[0]]

init = tf.global_variables_initializer()
sess = tf.Session()

writer = tf.summary.FileWriter("./logs/xor_logs", sess.graph)

sess.run(init)

t_start = time.clock()
for epoch in range(100001):
    sess.run(train_step, feed_dict={X: INPUT_XOR, Y: OUTPUT_XOR})
    if epoch % 10000 == 0:
        print("_"*80)
        print('Epoch: ', epoch)
        print('   y_estimated: ')
        for element in sess.run(y_estimated, feed_dict={X: INPUT_XOR, Y: OUTPUT_XOR}):
            print('    ',element)
        print('   W: ')
        for element in sess.run(W):
            print('    ',element)
        print('   c: ')
        for element in sess.run(c):
            print('    ',element)
        print('   w: ')
        for element in sess.run(w):
            print('    ',element)
        print('   b ')
        for element in sess.run(b):
            print('    ',element)
        print('   loss: ', sess.run(loss, feed_dict={X: INPUT_XOR, Y: OUTPUT_XOR}))
t_end = time.clock()
print("_"*80)
print('Elapsed time ', t_end - t_start)

