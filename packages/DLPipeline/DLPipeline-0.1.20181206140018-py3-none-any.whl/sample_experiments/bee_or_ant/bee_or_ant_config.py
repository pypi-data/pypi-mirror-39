#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dlpipeline.utilities.configurations.base_config import *
from pathlib import Path

__author__ = 'cnheider'
CONFIG_NAME = __name__
CONFIG_FILE = __file__

# DATASET_NAME

DATASET_NAME = 'beeorant'
EMBEDDING_MODULE = 'https://tfhub.dev/google/imagenet/inception_v3/feature_vector/1'
# EMBEDDING_MODULE = ('https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/2')

# PATHS

HOME_DIRECTORY = Path.home()
DATA_HOME = HOME_DIRECTORY / 'Datasets' / 'Classification'
LOGGING_DIRECTORY = HOME_DIRECTORY / 'Models'
DATASET_NAME_DIRECTORY = DATA_HOME / DATASET_NAME
IMAGE_DIRECTORY = DATASET_NAME_DIRECTORY / 'images'
EMBEDDING_DIRECTORY = DATASET_NAME_DIRECTORY / 'embeddings'

## LOGGING

MODEL_DIRECTORY = LOGGING_DIRECTORY / DATASET_NAME / TIME
CHECKPOINT_NAME = MODEL_DIRECTORY / 'retrain_checkpoint'
INTERMEDIATE_OUTPUT_GRAPHS_DIRECTORY = MODEL_DIRECTORY / 'intermediate_graph'
OUTPUT_LABELS_FILE_NAME = MODEL_DIRECTORY / 'output_labels.txt'
OUTPUT_GRAPH = MODEL_DIRECTORY / 'output_graph'
SAVE_MODEL_PATH = MODEL_DIRECTORY / 'export'
SUMMARIES_DIRECTORY = MODEL_DIRECTORY
SAVED_MODEL_DIRECTORY = MODEL_DIRECTORY / TIME

STEPS = 110
