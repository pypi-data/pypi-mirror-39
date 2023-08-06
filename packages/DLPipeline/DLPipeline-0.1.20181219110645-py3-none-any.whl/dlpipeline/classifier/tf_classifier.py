#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from dlpipeline.classifier.persistence.export import export_model
from dlpipeline.classifier.persistence.save import save_graph_to_file
from dlpipeline.classifier.tf_imp.classification_net import classification_net
from dlpipeline.classifier.tf_imp.evaluation import run_final_eval, evaluation_nodes
from dlpipeline.classifier.dlp_classifier import DLPClassifier

import numpy as np

from dlpipeline.utilities.path_utilities.directory_exists import ensure_directory_exists
from dlpipeline.visualiser.visualisation.confusion_matrix import plot_confusion_matrix

__author__ = 'cnheider'

from datetime import datetime

import tensorflow as tf


class TFClassifier(DLPClassifier):

  def _entry_point(self, data_iterator):
    return self._iterable

  def __init__(self, iterable: iter, *, input_size, output_size, C):
    super().__init__(iterable, C=C)

    self._C = C
    self._iterable = iterable
    self._classifier = classification_net(input_size=input_size,
                                          output_size=output_size,
                                          is_training=True,
                                          learning_rate=self._C.learning_rate)

    self._evaluation = evaluation_nodes(result_node=self._classifier.prediction_node,
                                        ground_truth_node=self._classifier.label_node)

    self._summary = tf.summary.merge_all()

    if tf.gfile.Exists(
        C.summaries_directory):  # Set up the directory we'll write summaries to for TensorBoard
      pass
      # tf.gfile.DeleteRecursively(summaries_directory)
    else:
      tf.gfile.MakeDirs(C.summaries_directory)

    if C.intermediate_store_frequency > 0:
      ensure_directory_exists(C.intermediate_output_graphs_directory)

  def learn(self,
            sess,
            *,
            module_specification,
            logging_interval=100,
            C=None,
            **kwargs):

    train_saver = tf.train.Saver()

    tf.logging.set_verbosity(tf.logging.INFO)

    train_writer = tf.summary.FileWriter(C.summaries_directory + 'training_set', sess.graph)
    validation_writer = tf.summary.FileWriter(C.summaries_directory + 'validation_set')

    for step_i in range(C.steps):
      (input_features, labels) = self._iterable.entry_point(self._iterable, sess=sess, set='training')

      train_summary, _ = sess.run([self._summary,
                                   self._classifier.train_step_node],
                                  feed_dict={self._classifier.input_node:input_features,
                                             self._classifier.label_node:labels
                                             }
                                  )

      train_writer.add_summary(train_summary, step_i)

      # region Validation

      if (step_i % C.eval_step_interval) == 0 or step_i + 1 == C.steps:
        train_accuracy, cross_entropy_value, cf_mat_value = sess.run([self._evaluation.accuracy,
                                                                      self._classifier.cross_entropy_node,
                                                                      self._evaluation.cf_mat],
                                                                     feed_dict={
                                                                       self._classifier.input_node:input_features,
                                                                       self._classifier.label_node:labels
                                                                       }
                                                                     )

        conf_mat = plot_confusion_matrix(labels=self._iterable.keys(),
                                         tensor_name='training/confusion_matrix',
                                         conf_mat=cf_mat_value)
        train_writer.add_summary(conf_mat, step_i)

        (validation_embeddings,
         validation_label,
         _) = self._iterable.entry_point(self._iterable,
                                          sess=sess,
                                          set='validation')

        (validation_summary,
         validation_accuracy,
         validation_cf_mat_value) = sess.run([self._summary,
                                              self._evaluation.accuracy,
                                              self._evaluation.cf_mat],
                                             feed_dict={
                                               self._classifier.input_node:validation_embeddings,
                                               self._classifier.label_node:validation_label
                                               }
                                             )

        validation_writer.add_summary(validation_summary, step_i)

        val_conf_mat = plot_confusion_matrix(
            labels=self._iterable.keys(),
            tensor_name='validation/confusion_matrix',
            conf_mat=validation_cf_mat_value)
        validation_writer.add_summary(val_conf_mat, step_i)

        if step_i % logging_interval == 0:
          tf.logging.info(f'{datetime.now()}: '
                          f'Step {step_i:d}: '
                          f'Train accuracy = {train_accuracy * 100:.1f}%%')
          tf.logging.info(f'{datetime.now()}: '
                          f'Step {step_i:d}: '
                          f'Cross entropy = {cross_entropy_value:f}')
          tf.logging.info(f'{datetime.now()}: '
                          f'Step {step_i:d}: '
                          f'Validation accuracy = {validation_accuracy * 100:.1f}%% '
                          f'(N={len(validation_embeddings):d})')

      # endregion

      if (C.intermediate_store_frequency > 0 and
          (step_i % C.intermediate_store_frequency == 0) and
          step_i > 0):
        self.intermediate_save(step_i,
                               self._iterable.class_count,
                               self._train_saver,
                               C,
                               module_specification=module_specification)

    train_saver.save(sess, C.checkpoint_name)

  def intermediate_save(self, i, class_count, train_saver, C, *, module_specification):
    '''
    # If we want to do an intermediate save,
    # save a checkpoint of the train graph, to restore into
    # the eval graph.
    '''
    train_saver.save(C.checkpoint_name)

    intermediate_file_name = os.path.join(C.intermediate_output_graphs_directory,
                                          f'intermediate_model_{i}.pb')

    tf.logging.info(f'Save intermediate result to : {intermediate_file_name}')

    save_graph_to_file(intermediate_file_name,
                       class_count=class_count,
                       checkpoint_name=C.checkpoint_name,
                       module_specification=module_specification)

  def save(self, dataset, C, module_specification, quantize=False):
    '''
    # Write out the trained graph and labels with the weights stored as constants.
    '''

    tf.logging.info(f'Save final result to : {C.output_graph}')
    if quantize:
      tf.logging.info('The classifier is instrumented for quantization with TF-Lite')

    save_graph_to_file(C.output_graph,
                       module_specification=module_specification,
                       class_count=dataset.class_count,
                       checkpoint_name=C.checkpoint_name)

    with tf.gfile.GFile(C.output_labels_file_name, 'w') as f:
      f.write('\n'.join(dataset.keys()) + '\n')

    if C.saved_model_directory:
      return export_model(class_count=dataset.class_count,
                   module_specification=module_specification,
                   **vars(C))

  def test(self,
           sess,
           dataset,
           C,
           *,
           embedder,
           graph_handles):
    run_final_eval(sess,
                   dataset=dataset,
                   jpeg_data_node=graph_handles.jpeg_placeholder,
                   resized_image_node=graph_handles.resized_image_node,
                   embedder=embedder,
                   **vars(C))

  @staticmethod
  def predict(sess,
              *,
              model_graph,
              input_tensor,
              **kwargs):
    input_node = model_graph.get_operation_by_name('resized_input_tensor_placeholder').outputs[0]
    output_node = model_graph.get_operation_by_name('module_apply_default/hub_output/feature_vector/SpatialSqueeze').outputs[0]

    results2 = sess.run(output_node, feed_dict={input_node:input_tensor})

    input_node2 = model_graph.get_operation_by_name('classifier/placeholders/features_placeholder').outputs[0]
    output_node2 = model_graph.get_operation_by_name('softmax_output').outputs[0]

    results = sess.run(output_node2, feed_dict={input_node2:results2})
    results = np.squeeze(results)
    return results
