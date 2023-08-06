import sys
import collections
import hashlib
import re
import tensorflow as tf

ACCEPTED_FORMATS = ['png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG', 'gif', 'GIF']


def test_validation_split(classes,
                          *,
                          testing_percentage=15,
                          validation_percentage=15):
  '''
  Magic hashing

  :param classes:
  :param testing_percentage:
  :param validation_percentage:
  :return:
  '''
  result = collections.OrderedDict()

  for label in classes:
    training_images = []
    testing_images = []
    validation_images = []

    for file_name in classes[label]:

      hash_name = re.sub(r'_nohash_.*$', '', file_name)
      hash_name_hashed = hashlib.sha1(tf.compat.as_bytes(hash_name)).hexdigest()
      percentage_hash = ((int(hash_name_hashed, 16) %
                          (sys.maxsize + 1)) *
                         (100.0 / sys.maxsize))

      if percentage_hash < validation_percentage:
        validation_images.append(file_name)
      elif percentage_hash < (testing_percentage + validation_percentage):
        testing_images.append(file_name)
      else:
        training_images.append(file_name)

    result[label] = {
      'training':  training_images,
      'testing':   testing_images,
      'validation':validation_images,
      }

  return result
