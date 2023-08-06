#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pathlib

__author__ = 'cnheider'


def load_lastest_model(path: str) -> str:
  '''
  Sorts the checkpoints by modification time and return the latest.

  :param path:
  :return:
  '''
  checkpoints = pathlib.Path(path).glob("*.index")
  checkpoints = sorted(checkpoints, key=lambda cp:cp.stat().st_mtime)
  checkpoints = [cp.with_suffix('') for cp in checkpoints]
  latest = str(checkpoints[-1])
  return latest
