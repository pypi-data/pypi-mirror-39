#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from typing import Generator

from dlpipeline import DLPDataIterator
from dlpipeline.classifier.tf_imp.classification_net import classification_net
from dlpipeline.classifier.tf_imp.evaluation import run_final_eval, evaluation_nodes
from dlpipeline.utilities.visualisation.confusion_matrix import plot_confusion_matrix
from dlpipeline.classifier.dlpclassifier import DLPClassifier
from dlpipeline.utilities.persistence.export import export_model
from dlpipeline.utilities.persistence.save import save_graph_to_file

__author__ = 'cnheider'

from datetime import datetime

import tensorflow as tf


class TFClassifier(DLPClassifier):
  def __init__(self, dataset: iter, *, augmentor, embedder, C):
    super().__init__(dataset, C=C)

    self._C = C
    self._dataset = dataset
    self.build(embedder)

    self._embedder = embedder
    self._transformer = augmentor

  def build(self, tf_hub_nodes):

    self.tf_config = tf.ConfigProto()
    self.tf_config.gpu_options.allow_growth = True
    self.tf_config.allow_soft_placement = True

    self.graph = tf_hub_nodes.graph
    #graph = tf.get_default_graph()
    with tf.Session(config=self.tf_config, graph=self.graph) as sess:
      self._classifier_handles = classification_net(input_size=tf_hub_nodes.embedding_size,
                                                    output_size=self._dataset.class_count,
                                                    batch_size=tf_hub_nodes.batch_size,
                                                    is_training=True,
                                                    learning_rate=self._C.learning_rate)

      self._eval_handles = evaluation_nodes(
          result_node=self._classifier_handles.prediction_node,
          ground_truth_node=self._classifier_handles.label_node)

      self._summary_handle = tf.summary.merge_all()



  def learn(self, dataset: DLPDataIterator, *, logging_interval=100, C=None):
    tf.logging.set_verbosity(tf.logging.INFO)

    with tf.Session(graph=self.graph, config=self.tf_config) as sess:
      sess.run(tf.global_variables_initializer())

      self._train_saver = tf.train.Saver()

      train_writer = tf.summary.FileWriter(C.summaries_directory + 'training_set', sess.graph)
      validation_writer = tf.summary.FileWriter(C.summaries_directory + 'validation_set')

      for step_i in range(C.steps):
        (input_features, labels) = self._embedder.fetch_data(self._transformer,
                                                             dataset,
                                                             C=C,
                                                             sub_set='training')

        train_summary, _ = sess.run([self._summary_handle,
                                     self._classifier_handles.train_step_node],
                                    feed_dict={self._classifier_handles.input_node:input_features,
                                               self._classifier_handles.label_node:labels
                                               }
                                    )

        train_writer.add_summary(train_summary, step_i)

        # region Validation

        if (step_i % C.eval_step_interval) == 0 or step_i + 1 == C.steps:
          train_accuracy, cross_entropy_value, cf_mat_value = sess.run([self._eval_handles.accuracy,
                                                                        self._classifier_handles.cross_entropy_node,
                                                                        self._eval_handles.cf_mat],
                                                                       feed_dict={
                                                                         self._classifier_handles.input_node:input_features,
                                                                         self._classifier_handles.label_node:labels
                                                                         }
                                                                       )

          conf_mat = plot_confusion_matrix(labels=dataset.keys(),
                                           tensor_name='training/confusion_matrix',
                                           conf_mat=cf_mat_value)
          train_writer.add_summary(conf_mat, step_i)

          (validation_embeddings,
           validation_label,
           _) = self._embedder.get_random_cached_embeddings(dataset,
                                                            'validation',
                                                            jpeg_data_tensor=self._transformer._transformation_nodes.jpeg_node,
                                                            decoded_image_tensor=self._transformer._transformation_nodes.decoded_image_node,
                                                            batch_size=self._C.train_batch_size
                                                            )

          (validation_summary,
           validation_accuracy,
           validation_cf_mat_value) = sess.run([self._summary_handle,
                                                self._eval_handles.accuracy,
                                                self._eval_handles.cf_mat],
                                               feed_dict={
                                                 self._classifier_handles.input_node:validation_embeddings,
                                                 self._classifier_handles.label_node:validation_label
                                                 }
                                               )

          validation_writer.add_summary(validation_summary, step_i)

          val_conf_mat = plot_confusion_matrix(
              labels=dataset.keys(),
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

        if C.intermediate_store_frequency > 0 and (
            step_i % C.intermediate_store_frequency == 0) and step_i > 0:
          self.intermediate_save(step_i, dataset.class_count, self._train_saver, C)

      self._train_saver.save(sess, C.checkpoint_name)

  def intermediate_save(self, i, class_count, train_saver, C):
    '''
    # If we want to do an intermediate save,
    # save a checkpoint of the train graph, to restore into
    # the eval graph.
    '''
    train_saver.save(C.checkpoint_name)

    intermediate_file_name = os.path.join(C.intermediate_output_graphs_directory, f'intermediate_{i}.pb')

    tf.logging.info(f'Save intermediate result to : {intermediate_file_name}')

    save_graph_to_file(intermediate_file_name,
                       class_count=class_count,
                       checkpoint_name=C.checkpoint_name,
                       module_spec=self._embedder.module_spec)

  def save(self, dataset, C):
    '''
    # Write out the trained graph and labels with the weights stored as constants.
    '''

    tf.logging.info(f'Save final result to : {C.output_graph}')
    if self._embedder.quantize:
      tf.logging.info('The classifier is instrumented for quantization with TF-Lite')

    save_graph_to_file(C.output_graph,
                       module_spec=self._embedder.module_spec,
                       class_count=dataset.class_count,
                       checkpoint_name=C.checkpoint_name)

    with tf.gfile.GFile(C.output_labels_file_name, 'w') as f:
      f.write('\n'.join(dataset.keys()) + '\n')

    if C.saved_model_directory:
      export_model(class_count=dataset.class_count, module_spec=self._embedder.module_spec, **vars(C))

  def test(self, dataset, C):

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.allow_soft_placement = True

    with tf.Session(config=config) as sess:
      run_final_eval(
          dataset=dataset,
          jpeg_data_node=self._transformer._transformation_nodes.jpeg_node,
          decoded_image_node=self._transformer._transformation_nodes.decoded_image_node,
          resized_image_node=self._embedder.resized_image_node,
          embedding_node=self._embedder.embedding_node,
          module_spec=self._embedder.module_spec,
          embedder=self._embedder,
          **vars(C))

  def predict(self,
              model_graph,
              input_tensor,
              input_layer_name="input",
              output_layer_name="InceptionV3/Predictions/Reshape_1",
              **kwargs):
    input_name = f'import/{input_layer_name}'
    output_name = f'import/{output_layer_name}'
    print(model_graph.get_operations())
    input_node = model_graph.get_operation_by_name(input_name)
    output_node = model_graph.get_operation_by_name(output_name)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.allow_soft_placement = True

    with tf.Session(config=config, graph=model_graph) as sess:
      results = sess.run(output_node.outputs[0],
                         {
                           input_node.outputs[0]:input_tensor
                           }
                         )
    results = np.squeeze(results)
    return results