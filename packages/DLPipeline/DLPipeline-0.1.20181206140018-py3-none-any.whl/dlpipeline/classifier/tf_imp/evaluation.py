import tensorflow as tf
from warg import NamedOrderedDictionary
import tensorflow_hub as hub

from dlpipeline.classifier.tf_imp.classification_net import classification_net

# A module is understood as instrumented for quantization with TF-Lite
# if it contains any of these ops.
FAKE_QUANT_OPS = ('FakeQuantWithMinMaxVars',
                  'FakeQuantWithMinMaxVarsPerChannel')


def build_eval_session(*,
                       module_spec,
                       class_count,
                       checkpoint_name
                       ):
  '''

  Builds an restored eval session without train operations for exporting.

  Args:
    module_spec: The hub.ModuleSpec for the image module being used.
    class_count: Number of classes

  Returns:
    Eval session containing the restored eval graph.
    The embedding input, ground truth, eval step, and prediction tensors.
    :param module_spec:
    :param class_count:
    :param learning_rate:
    :param checkpoint_name:
    :param final_node_name:
  '''

  height, width = hub.get_expected_image_size(module_spec)
  depth = 3

  with tf.Graph().as_default() as graph:
    resized_input_tensor = tf.placeholder(tf.float32, [None, height, width, depth])

    module = hub.Module(module_spec)
    embedding_output_node = module(resized_input_tensor)
    quantize = any(node.op in FAKE_QUANT_OPS
                   for node in graph.as_graph_def().node)

  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  config.allow_soft_placement = True

  eval_sess = tf.Session(config=config, graph=graph)
  with graph.as_default():
    batch_size, embedding_size = embedding_output_node.get_shape().as_list()

    # Add the new layer for exporting.
    (_,
     _,
     embedding_input_node,
     ground_truth_input_node,
     output_node) = classification_net(embedding_output_node=embedding_output_node,
                                       input_size=embedding_size,
                                       output_size=class_count,
                                       batch_size=batch_size,
                                       is_training=False,
                                       quantize=quantize)



    tf.train.Saver().restore(eval_sess, checkpoint_name)
    # Now we need to restore the values from the training graph to the eval graph.

    ev = evaluation_nodes(result_node=output_node,
                                                                 ground_truth_node=ground_truth_input_node)

  return NamedOrderedDictionary(eval_session=eval_sess,
                                resized_input_tensor=resized_input_tensor,
                                embedding_input_node=embedding_input_node,
                                ground_truth_input_node=ground_truth_input_node,
                                evaluation_step_node=ev.accuracy,
                                prediction_node=ev.prediction
  ,graph=graph
                              )


def run_final_eval(module_spec,
                   dataset,
                   jpeg_data_node,
                   decoded_image_node,
                   embedder_input_node,
                   embedding_output_node,
                   *,
                   checkpoint_name,
                   test_batch_size,
                   embedding_directory,
                   embedding_module,
                   embedder,
                   print_misclassified=True,
                   **kwargs):
  '''Runs a final evaluation on an eval graph using the test data set.

  Args:
    train_session: Session for the train graph with the tensors below.
    module_spec: The hub.ModuleSpec for the image module being used.
    class_count: Number of classes
    dataset: OrderedDict of training images for each label.
    jpeg_data_node: The layer to feed jpeg image data into.
    decoded_image_node: The output of decoding and resizing the image.
    embedder_input_node: The input node of the recognition graph.
    embedding_output_node: The embedding output layer of the CNN graph.
    :param checkpoint_name:
  '''

  (test_embeddings,
   test_ground_truth,
   test_filenames) = embedder.get_random_cached_embeddings(dataset,
                                                  'testing',
                                                  jpeg_data_tensor=jpeg_data_node,
                                                  decoded_image_tensor=decoded_image_node,
                                                  resized_input_tensor=embedder_input_node,
                                                  embedding_output_node=embedding_output_node,
                                                  embedding_module=embedding_module,
                                                  batch_size=test_batch_size,
                                                  embedding_directory=embedding_directory)

  ev = build_eval_session(module_spec=module_spec,
                                         class_count=dataset.class_count,
                                         checkpoint_name=checkpoint_name)

  test_accuracy, predictions = ev.eval_session.run([ev.evaluation_step_node, ev.prediction_node],
                                                feed_dict={
                                                  ev.embedding_input_node:test_embeddings,
                                                  ev.ground_truth_input_node:  test_ground_truth
                                                  })

  tf.logging.info(f'Final test accuracy = {test_accuracy * 100:.1f}%% (N={len(test_embeddings):d})')

  if print_misclassified:
    tf.logging.info('=== Results ===')
    for i, test_filename in enumerate(test_filenames):
      if predictions[i] != test_ground_truth[i]:
        tf.logging.info(f'{test_filename:>70}  {list(dataset.keys())[predictions[i]]}')
      else:
        tf.logging.info(f'{test_filename:>70} prediction {predictions[i]} matches '
                        f'ground truth {test_ground_truth[i]}')


def evaluation_nodes(*,
                     result_node,
                     ground_truth_node):
  '''
  Inserts the operations we need to evaluate the accuracy of our results.

  Args:
    result_node: The new final node that produces results.
    ground_truth_node: The node we feed ground truth data
    into.

  Returns:
    Tuple of (evaluation step, prediction).
  '''
  with tf.name_scope('accuracy'):
    with tf.name_scope('correct_prediction'):
      prediction_node = tf.argmax(result_node, 1)
      correct_prediction = tf.equal(ground_truth_node, prediction_node)
      cf_mat = tf.confusion_matrix(ground_truth_node, prediction_node)
    with tf.name_scope('accuracy'):
      evaluation_step_node = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

  tf.summary.scalar('accuracy', evaluation_step_node)

  return NamedOrderedDictionary(accuracy=evaluation_step_node,
                                prediction=prediction_node,
                                cf_mat=cf_mat)
