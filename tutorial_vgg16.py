#! /usr/bin/python
# -*- coding: utf8 -*-


import tensorflow as tf
import tensorlayer as tl
import os
import sys
import numpy as np
import time
from scipy.misc import imread, imresize
from data.imagenet_classes import *

"""
VGG-16 in TensorLayer

Introduction
----------------
VGG is a convolutional neural network model proposed by K. Simonyan and A. Zisserman
from the University of Oxford in the paper “Very Deep Convolutional Networks for
Large-Scale Image Recognition”  . The model achieves 92.7% top-5 test accuracy in ImageNet,
which is a dataset of over 14 million images belonging to 1000 classes.

Download Pre-trained Model
----------------------------
Model weights - vgg16_weights.npz http://www.cs.toronto.edu/~frossard/post/vgg16/

"""


def conv_layers(net_in):
    with tf.name_scope('preprocess') as scope:
        """
        Notice that we include a preprocessing layer that takes the RGB image
        with pixels values in the range of 0-255 and subtracts the mean image
        values (calculated over the entire ImageNet training set).
        """
        mean = tf.constant([123.68, 116.779, 103.939], dtype=tf.float32, shape=[1, 1, 1, 3], name='img_mean')
        net_in.outputs = net_in.outputs - mean
    """ conv1 """
    network = tl.layers.Conv2dLayer(net_in,
                    act = tf.nn.relu,
                    shape = [3, 3, 3, 64],  # 64 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv1_1')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 64, 64],  # 64 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv1_2')
    network = tl.layers.PoolLayer(network,
                    ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1],
                    padding='SAME',
                    pool = tf.nn.max_pool,
                    name ='pool1')
    """ conv2 """
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 64, 128],  # 128 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv2_1')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 128, 128],  # 128 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv2_2')
    network = tl.layers.PoolLayer(network,
                    ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1],
                    padding='SAME',
                    pool = tf.nn.max_pool,
                    name ='pool2')
    """ conv3 """
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 128, 256],  # 256 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv3_1')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 256, 256],  # 256 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv3_2')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 256, 256],  # 256 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv3_3')
    network = tl.layers.PoolLayer(network,
                    ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1],
                    padding='SAME',
                    pool = tf.nn.max_pool,
                    name ='pool3')
    """ conv4 """
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 256, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv4_1')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 512, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv4_2')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 512, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv4_3')
    network = tl.layers.PoolLayer(network,
                    ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1],
                    padding='SAME',
                    pool = tf.nn.max_pool,
                    name ='pool4')
    """ conv5 """
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 512, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv5_1')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 512, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv5_2')
    network = tl.layers.Conv2dLayer(network,
                    act = tf.nn.relu,
                    shape = [3, 3, 512, 512],  # 512 features for each 3x3 patch
                    strides = [1, 1, 1, 1],
                    W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                    b_init = tf.constant_initializer(value=0.0),
                    padding='SAME',
                    name ='conv5_3')
    network = tl.layers.PoolLayer(network,
                    ksize=[1, 2, 2, 1],
                    strides=[1, 2, 2, 1],
                    padding='SAME',
                    pool = tf.nn.max_pool,
                    name ='pool5')
    return network


def fc_layers(net):
    network = tl.layers.FlattenLayer(net, name='flatten')
    network = tl.layers.DenseLayer(network, n_units=4096,
                        act = tf.nn.relu,
                        W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                        b_init = tf.constant_initializer(value=0.0),
                        name = 'fc1_relu')
    network = tl.layers.DenseLayer(network, n_units=4096,
                        act = tf.nn.relu,
                        W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                        b_init = tf.constant_initializer(value=0.0),
                        name = 'fc2_relu')
    network = tl.layers.DenseLayer(network, n_units=1000,
                        act = tf.identity,
                        W_init = tf.truncated_normal_initializer(mean=0.0, stddev=1e-1, seed=None, dtype=tf.float32),
                        b_init = tf.constant_initializer(value=0.0),
                        name = 'fc3_relu')
    return network


sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, [None, 224, 224, 3])
y_ = tf.placeholder(tf.int32, shape=[None, ], name='y_')

net_in = tl.layers.InputLayer(x, name='input_layer')
net_cnn = conv_layers(net_in)
network = fc_layers(net_cnn)

y = network.outputs
probs = tf.nn.softmax(y)
y_op = tf.argmax(tf.nn.softmax(y), 1)
cost = tl.cost.cross_entropy(y, y_)

correct_prediction = tf.equal(tf.cast(tf.argmax(y, 1), tf.float32), tf.cast(y_, tf.float32))
acc = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())
network.print_params()
network.print_layers()

# you need to download the model from http://www.cs.toronto.edu/~frossard/post/vgg16/
npz = np.load('vgg16_weights.npz')

params = []
for val in sorted( npz.items() ):
    print("  Loading %s" % str(val[1].shape))
    params.append(val[1])

tl.files.assign_params(sess, params, network)

img1 = imread('data/laska.png', mode='RGB')
img1 = imresize(img1, (224, 224))

start_time = time.time()
prob = sess.run(probs, feed_dict={x: [img1]})[0]
print("  End time : %.5ss" % (time.time() - start_time))
preds = (np.argsort(prob)[::-1])[0:5]
for p in preds:
    print(class_names[p], prob[p])









#
