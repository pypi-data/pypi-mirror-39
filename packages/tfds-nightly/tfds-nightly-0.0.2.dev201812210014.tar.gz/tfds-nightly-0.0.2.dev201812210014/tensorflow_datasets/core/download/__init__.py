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

"""Public API of the download manager."""

from tensorflow_datasets.core.download.download_manager import DownloadManager
from tensorflow_datasets.core.download.extractor import iter_gzip
from tensorflow_datasets.core.download.extractor import iter_tar
from tensorflow_datasets.core.download.extractor import iter_tar_gz
from tensorflow_datasets.core.download.extractor import iter_zip
from tensorflow_datasets.core.download.util import GenerateMode

__all__ = [
    "DownloadManager",
    "GenerateMode",
    "iter_gzip",
    "iter_tar",
    "iter_tar_gz",
    "iter_zip",
]
