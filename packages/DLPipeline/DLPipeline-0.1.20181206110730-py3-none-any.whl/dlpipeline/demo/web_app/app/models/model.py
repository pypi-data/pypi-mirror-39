import json
import pickle as pk

import numpy as np
from dlpipeline.demo.load import load_graph
from retinalyze.test_model import predict
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import img_to_array, load_img
# Load models and support
from tensorflow.python.keras.applications.imagenet_utils import preprocess_input
from tensorflow.python.keras.backend import clear_session
from tensorflow.python.keras.utils import get_file

with open('models/vgg16_cat_list.pk', 'rb') as f:
  cat_list = pk.load(f)

CLASS_INDEX = None
CLASS_INDEX_PATH = 'https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json'
# CLASS_INDEX_PATH = 'imagenet_class_index.json'
classier = load_graph('/home/captain/Projects/IBBD5/dlpipeline/exclude/inception_v3_2016_08_28_frozen.pb')
clear_session()


def get_predictions(predictions, top=5):
  global CLASS_INDEX
  if len(predictions.shape) != 2 or predictions.shape[1] != 1000:
    raise ValueError(
        f'`decode_predictions` expects a batch of predictions (i.e. a 2D array of shape (samples, '
        f'1000)). Found array with shape: {predictions.shape}')
  if CLASS_INDEX is None:
    file_path = get_file('imagenet_class_index.json',
                         CLASS_INDEX_PATH,
                         cache_subdir='models')
    CLASS_INDEX = json.load(open(file_path))
  l = []
  for prediction in predictions:
    top_indices = prediction.argsort()[-top:][::-1]
    indexes = [tuple(CLASS_INDEX[str(i)]) + (prediction[i],) for i in top_indices]
    indexes.sort(key=lambda x:x[2], reverse=True)
    l.append(indexes)
  return l


def prepare_img_224(img_path):
  img = load_img(img_path, target_size=(224, 224))
  x = img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  return x


def get_predicted_categories(img_224) -> list:
  image_net_model = VGG16(weights='imagenet')
  out = image_net_model.predict(img_224)
  topn = get_predictions(out, top=5)
  return topn


def prepare_img_size(img_path, size=299):
  img = load_img(img_path, target_size=(size, size))  # this is a PIL image
  x = img_to_array(img)  # this is a Numpy array with shape (3, 256, 256)
  x = x.reshape((1,) + x.shape) / 255
  return x


def run_model(img_path):
  img_224 = prepare_img_224(img_path)
  top_n_prediction = get_predicted_categories(img_224)

  img_256 = prepare_img_size(img_path)
  category_result = predict(classier, img_256)

  x = 0
  y = 0

  zipped = [a for a in zip(*top_n_prediction[0])]
  zz = ''.join([f'{cat}: {prob},\n\n' for cat, prob in zip(zipped[1],
                                                           zipped[2])])

  zz2 = category_result

  result = {'model1_name':  'Vgg Categories',
            'model1_result':zz,
            'model2_name':  'Model prediction',
            'model2_result':zz2,
            'message':      'Assessment complete!'
            }
  return result
