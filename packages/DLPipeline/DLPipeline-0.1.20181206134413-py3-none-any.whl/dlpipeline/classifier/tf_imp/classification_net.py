#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline import NamedOrderedDictionary
from dlpipeline.visualiser.tfvisualiser import TFVisualiser

__author__ = 'cnheider'

import tensorflow as tf


def classification_net(*,
                       input_size,
                       output_size,
                       is_training,
                       batch_size=None,
                       learning_rate=0,
                       quantize=False,
                       stddev=0.001,
                       hidden_layers=(),#(64,32),
                       visualiser=TFVisualiser(),
                       **kwargs):
  '''
  Adds a new softmax and fully-connected layer for training and eval.

  We need to retrain the top layer to identify our new classes, so this function
  adds the right operations to the graph, along with some variables to hold the
  weights, and then sets up all the gradients for the backward pass.

  The set up for the softmax and fully-connected layers is based on:
  https://www.tensorflow.org/tutorials/mnist/beginners/index.html

  Args:
    class_count: Integer of how many categories of things we're trying to
        recognize.
    final_node_name: Name string for the new final node that produces results.
    embedding_output_node: The output of the main CNN graph.
    quantize_layer: Boolean, specifying whether the newly added layer should be
        instrumented for quantization with TF-Lite.
    is_training: Boolean, specifying whether the newly add layer is for training
        or eval.

  Returns:
    The tensors for the training and cross entropy results, and tensors for the
    embedding input and ground truth input.
    :param visualiser:
    :param embedding_output_node:
    :param output_size:
    :param input_size:
    :param quantize:
    :param is_training:
    :param output_node_name:
    :param learning_rate:
  '''

  assert batch_size is None

  with tf.name_scope('placeholders'):
    input_tensor = tf.placeholder(tf.float32,
                                  shape=[batch_size, input_size],
                                  name='input_placeholder'
                                  )

    label_tensor = tf.placeholder(tf.int64, shape=[batch_size], name='label_placeholder')

  with tf.name_scope('classifier'):

    last_layer_node = input_tensor
    last_layer_size = input_size

    with tf.name_scope(f'hidden_layers'):
      for layer_size,i in zip(hidden_layers,range(len(hidden_layers))):

        with tf.name_scope(f'weights{i}'):
          initial_value = tf.truncated_normal([last_layer_size, layer_size], stddev=stddev)
          layer_weights = tf.Variable(initial_value, name='weights')
          visualiser.visualise_variable(layer_weights)

        with tf.name_scope(f'biases{i}'):
          layer_biases_out = tf.Variable(tf.zeros([layer_size]), name='biases')
          visualiser.visualise_variable(layer_biases_out)

        with tf.name_scope(f'Wx_plus_b{i}'):
          mul = tf.matmul(last_layer_node, layer_weights) + layer_biases_out
          tf.summary.histogram(f'mul', last_layer_node)
          last_layer_node = tf.nn.relu(mul)
          tf.summary.histogram(f'activations', last_layer_node)

        last_layer_size = layer_size

      '''
      hidden_layers2 = [hidden_layer_size//2]

      for units in hidden_layers2:
        last_layer_node = tf.layers.dense(last_layer_node, units=units, activation=tf.nn.relu)

      last_layer_size = hidden_layer_size//2
      '''

    with tf.name_scope('weights_out'):
      initial_value_out = tf.truncated_normal([last_layer_size, output_size], stddev=stddev)
      layer_weights_out = tf.Variable(initial_value_out, name='weights')
      visualiser.visualise_variable(layer_weights_out)

    with tf.name_scope('biases_out'):
      layer_biases_out = tf.Variable(tf.zeros([output_size]), name='biases')
      visualiser.visualise_variable(layer_biases_out)

    with tf.name_scope('Wx_plus_b_out'):
      logits = tf.matmul(last_layer_node, layer_weights_out) + layer_biases_out
      tf.summary.histogram('logits', logits)

  softmax_node = tf.nn.softmax(logits, name='softmax_output')

  if quantize:
    if is_training:
      tf.quantize.create_training_graph()
    else:
      tf.quantize.create_eval_graph()

  tf.summary.histogram(f'softmax_output_activations', softmax_node)

  if not is_training:  # If this is an eval graph, we don't need to add loss ops or an optimizer.
    return None, None, input_tensor, label_tensor, softmax_node

  cross_entropy_scope = 'cross_entropy_loss'
  with tf.name_scope(cross_entropy_scope):
    cross_entropy_mean_node = tf.losses.sparse_softmax_cross_entropy(labels=label_tensor,
                                                                     logits=logits)

  tf.summary.scalar(cross_entropy_scope, cross_entropy_mean_node)

  with tf.name_scope('optimiser'):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train_step_node = optimizer.minimize(cross_entropy_mean_node)

  return NamedOrderedDictionary(train_step_node=train_step_node,
                                cross_entropy_node=cross_entropy_mean_node,
                                input_node=input_tensor,
                                label_node=label_tensor,
                                prediction_node=softmax_node)


