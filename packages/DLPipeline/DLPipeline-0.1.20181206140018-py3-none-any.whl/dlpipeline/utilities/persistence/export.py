#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.classifier.tf_imp.evaluation import build_eval_session

__author__ = 'cnheider'

import tensorflow as tf


def export_model(module_spec,
                 class_count,
                 *,
                 checkpoint_name,
                 saved_model_directory,
                 output_node_name='softmax_output',
                 **kwargs):
  '''Exports classifier for serving.

  Args:
    module_spec: The hub.ModuleSpec for the image module being used.
    class_count: The number of classes.
    saved_model_directory: Directory in which to save exported classifier and variables.
    :param output_node_name:
  '''
  # The SavedModel should hold the eval graph.
  ss = build_eval_session(module_spec=module_spec,
                                            class_count=class_count,
                                            checkpoint_name=checkpoint_name)

  sess = ss.eval_session
  in_image = ss.resized_input_tensor

  with sess.graph.as_default() as graph:
    tf.saved_model.simple_save(sess,
                               saved_model_directory,
                               inputs={'image':in_image},
                               outputs={'prediction':graph.get_tensor_by_name(f'{output_node_name}:0')},
                               legacy_init_op=tf.group(tf.tables_initializer(), name='legacy_init_op')
                               )
