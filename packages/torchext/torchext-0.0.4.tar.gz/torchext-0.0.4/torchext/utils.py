# Copyright 2018 Yongjin Cho
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
import os
import glob
import time
import logging
import argparse
import subprocess
from collections import defaultdict

import torch


_checkpoint_file_prefix = "checkpoint"


def get_checkpoint_filepaths(model_dir):
    filepaths = glob.glob("{}/{}-*".format(model_dir, _checkpoint_file_prefix))
    filepaths.sort()
    return filepaths


def save_checkpoint(model_dir, step, states, keep_max=None):
    filepath = os.path.join(model_dir, "{}-{:08d}.pt".format(_checkpoint_file_prefix, step))
    logging.info("Saving the checkpoint to {}".format(filepath))
    torch.save(states, filepath)

    filepaths = get_checkpoint_filepaths(model_dir)
    if keep_max and len(filepaths) > keep_max:
        for filepath in filepaths[:len(filepaths) - keep_max]:
            os.remove(filepath)


def load_checkpoint(model_dir):
    filepaths = get_checkpoint_filepaths(model_dir)
    if not filepaths:
        return None
    latest_file = filepaths[-1]
    logging.info("Loading the checkpoint file: {}".format(latest_file))
    return torch.load(latest_file)


def check_git_hash(model_dir):
    status, cur_hash = subprocess.getstatusoutput("git rev-parse HEAD")
    if status != 0:
        logging.warn("It is not possible to compare versions of source and model, "
                     "because here is not a git repository.")
        return

    path = os.path.join(model_dir, "githash")
    if os.path.exists(path):
        saved_hash = open(path).read()
        if saved_hash != cur_hash:
            logging.warn("git hash values are different. {}(saved) != {}(current)".format(
                saved_hash[:8], cur_hash[:8]))
    else:
        open(path, "w").write(cur_hash)


def redirect_log_to_file(model_dir,
        level=logging.INFO,
        format='%(levelname)s\t%(asctime)s\t%(message)s',
        filename="train.log"):
    logger = logging.getLogger()

    formatter = logging.Formatter('%(levelname)s\t%(asctime)s\t%(message)s')

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    h = logging.FileHandler(os.path.join(model_dir, filename))
    h.setLevel(level)
    h.setFormatter(formatter)
    logger.addHandler(h)


def get_argument_parser(description=None):
    parser = argparse.ArgumentParser(description)
    parser.add_argument("-m", "--model_dir", type=str, required=True,
            help="The directory where the trained model will be saved.")
    parser.add_argument("-c", "--configs", default=[], nargs="*",
            help="A list of configuration items. "
                 "An item is a file path or a 'key=value' formatted string.")
    return parser


def parse_args(description=None):
    parser = get_argument_parser(description)
    args = parser.parse_args()
    return args


class Stopwatch:
    def __init__(self, start=False):
        self.start_time = None
        self.start()

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            return 0.0
        end = time.time()
        elapsed = end - self.start_time
        return elapsed

    def reset(self):
        self.start_time = None


class Stats:
    def __init__(self):
        self.reset_all()
        self.stopwatch = Stopwatch()

    def reset_all(self):
        self.samples = defaultdict(list)

    def add(self, **kwargs):
        for name, value in kwargs.items():
            if isinstance(value, torch.Tensor):
                value = value.detach().cpu().numpy()
            self.samples[name].append(value)

    def start_watch(self):
        self.stopwatch.start()

    def stop_watch(self):
        elapsed = self.stopwatch.stop()
        self.add(step_per_sec=1/elapsed)

    def mean(self, *args):
        result = {}
        for name in args:
            samples = self.samples[name]
            result[name] = sum(samples) / len(samples)
        return result

    def mean_all(self, reset=False):
        result = self.mean(*self.samples.keys())
        if reset:
            self.reset_all()
        return result
