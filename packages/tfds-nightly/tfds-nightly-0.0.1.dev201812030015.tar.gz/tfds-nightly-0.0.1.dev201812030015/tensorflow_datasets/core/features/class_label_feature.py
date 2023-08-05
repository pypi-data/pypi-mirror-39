# coding=utf-8
# Copyright 2018 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ClassLabel feature."""

import os
import six
import tensorflow as tf
from tensorflow_datasets.core import api_utils
from tensorflow_datasets.core.features import feature


class ClassLabel(feature.FeatureConnector):
  """Feature encoding an integer class label."""

  @api_utils.disallow_positional_args
  def __init__(self, num_classes=None, names=None, names_file=None):
    """Constructs a ClassLabel FeatureConnector.

    There are 3 ways to define a ClassLabel, which correspond to the 3
    arguments:
     * `num_classes`: create 0 to (num_classes-1) labels
     * `names`: a list of label strings
     * `names_file`: a file containing the list of labels.

    Note: On python2, the strings are encoded as utf-8.

    Args:
      num_classes: `int`, number of classes. All labels must be < num_classes.
      names: `list<str>`, string names for the integer classes. The
        order in which the names are provided is kept.
      names_file: `str`, path to a file with names for the integer
        classes, one per line.
    """
    self._num_classes = None
    self._str2int = None
    self._int2str = None

    # The label is explicitly set as undefined (no label defined)
    if not sum(bool(a) for a in (num_classes, names, names_file)):
      return

    if sum(bool(a) for a in (num_classes, names, names_file)) != 1:
      raise ValueError(
          "Only a single argument of ClassLabel() should be provided.")

    if num_classes:
      self._num_classes = num_classes
    else:
      self.names = names or _load_names_from_file(names_file)

  @property
  def num_classes(self):
    return self._num_classes

  @property
  def names(self):
    if not self._int2str:
      return None
    return list(self._int2str)

  @names.setter
  def names(self, new_names):
    # Names can only be defined once
    if self._int2str is not None:
      raise ValueError("Trying to overwrite already defined ClassLabel names.")

    # Set-up new names
    self._int2str = [tf.compat.as_text(name) for name in new_names]
    self._str2int = {name: i for i, name in enumerate(self._int2str)}

    # If num_classes has been defined, ensure that num_classes and names match
    num_classes = len(self._str2int)
    if self._num_classes is None:
      self._num_classes = num_classes
    elif self._num_classes != num_classes:
      raise ValueError(
          "ClassLabel number of names do not match the defined num_classes. "
          "Got {} names VS {} num_classes".format(
              num_classes, self._num_classes)
      )

  def str2int(self, str_value):
    """Conversion class name string => integer."""
    if not self._str2int:
      raise ValueError(
          "ClassLabel.str2int is not available because names haven't been "
          "defined in the ClassLabel constructor.")
    return self._str2int[tf.compat.as_text(str_value)]

  def int2str(self, int_value):
    """Conversion integer => class name string."""
    if not self._int2str:
      raise ValueError(
          "ClassLabel.int2str is not available because names haven't been "
          "defined in the ClassLabel constructor.")
    # Maybe should support batched np array/eager tensors, to allow things like
    # out_ids = model(inputs)
    # labels = cifar10.info.features['label'].int2str(out_ids)
    return self._int2str[int_value]

  def get_tensor_info(self):
    return feature.TensorInfo(shape=(), dtype=tf.int64)

  def encode_sample(self, sample_data):
    if self._num_classes is None:
      raise ValueError(
          "Trying to use ClassLabel feature with undefined number of class. "
          "Please set ClassLabel.names or num_classes."
      )

    # If a string is given, convert to associated integer
    if isinstance(sample_data, six.string_types):
      sample_data = self.str2int(sample_data)

    # Allowing -1 to mean no label.
    if not -1 <= sample_data < self._num_classes:
      raise ValueError("Class label %d greater than configured num_classes %d" %
                       (sample_data, self._num_classes))
    return sample_data

  def decode_sample(self, tfexample_data):
    return tf.reshape(tfexample_data, tuple())

  def save_metadata(self, data_dir, feature_name=None):
    """See base class for details."""
    # Save names if defined
    if self.names is not None:
      names_filepath = _get_names_filepath(data_dir, feature_name)
      _write_names_to_file(names_filepath, self.names)

  def load_metadata(self, data_dir, feature_name=None):
    """See base class for details."""
    # Restore names if defined
    names_filepath = _get_names_filepath(data_dir, feature_name)
    if tf.gfile.Exists(names_filepath):
      self.names = _load_names_from_file(names_filepath)


def _get_names_filepath(data_dir, feature_name):
  return os.path.join(data_dir, "{}.labels.txt".format(feature_name))


def _load_names_from_file(names_filepath):
  with tf.gfile.Open(names_filepath, "r") as f:
    return [
        name.strip()
        for name in tf.compat.as_text(f.read()).split("\n")
        if name.strip()  # Filter empty names
    ]


def _write_names_to_file(names_filepath, names):
  with tf.gfile.Open(names_filepath, "w") as f:
    f.write("\n".join(names) + "\n")
