#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from pathlib import Path

__author__ = 'cnheider'
PROJECT = 'DLPipeline'
CONFIG_NAME = __name__
CONFIG_FILE = __file__
TIME = str(time.time())

# EMBEDDING https://tfhub.dev/
USE_EMBEDDING = False
EMBEDDING_MODULE = 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1'
# EMBEDDING_MODULE = ('https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2')

# PATHS

HOME_DIRECTORY = Path.home()
DATA_HOME = HOME_DIRECTORY / 'Nextcloud/Visual Computing Lab/Projects/IBBD5/Data'
LOGGING_DIRECTORY = HOME_DIRECTORY / 'Models'

# TRAINING

TESTING_PERCENTAGE = 0
VALIDATION_PERCENTAGE = 25
VALIDATION_BATCH_SIZE = 100
STEPS = 10000
LEARNING_RATE = 3e-5
EPOCHS = 7
TRAIN_BATCH_SIZE = 64

# EVALUATION
N_SAMPLES = 10
TOP_N_PREDICTIONS = 5

RANDOM_SCALE = 0
RANDOM_BRIGHTNESS = 0
RANDOM_CROP = 0.0
FLIP_LEFT_RIGHT = False
FINAL_NODE_NAME = 'final_result'

INTERMEDIATE_STORE_FREQUENCY = 0

EVAL_STEP_INTERVAL = 10
TEST_BATCH_SIZE = -1

CHECKPOINT_INTERVAL = 5
VERBOSITY_LEVEL = 1
PRINT_MISCLASSIFIED = False
