import argparse
import os
import tarfile
import urllib

import tensorflow as tf


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())

  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()

  for l in proto_as_ascii_lines:
    label.append(l.rstrip())

  return label


def image_to_tensor(file_name,
                    input_height=299,
                    input_width=299,
                    input_mean=0,
                    input_std=255):
  input_name = "file_reader"
  # output_name = "normalized"
  file_reader = tf.read_file(file_name,
                             input_name)

  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader,
                                       channels=3,
                                       name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(
        tf.image.decode_gif(file_reader,
                            name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader,
                                       name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(file_reader,
                                        channels=3,
                                        name="jpeg_reader")
  float_caster = tf.cast(image_reader,
                         tf.float32)
  dims_expander = tf.expand_dims(float_caster,
                                 0)
  resized = tf.image.resize_bilinear(dims_expander,
                                     [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized,
                                     [input_mean]
                                     ),
                         [input_std])

  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  config.allow_soft_placement = True

  with tf.Session(config=config) as sess:
    result = sess.run(normalized)

  return result


def maybe_download_and_extract(data_url):
  '''Download and extract model tar file.
  If the pretrained model we're using doesn't already exist, this function
  downloads it from the TensorFlow.org website and unpacks it into a directory.
  Args:
    data_url: Web location of the tar file containing the pretrained model.
  '''

  dest_directory = ''
  if not os.path.exists(dest_directory):
    os.makedirs(dest_directory)
  filename = data_url.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    filepath, _ = urllib.request.urlretrieve(data_url, filepath)
    tarfile.open(filepath, 'r:gz').extractall(dest_directory)
