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
"""Conriguration Management Module
"""

_config_file_name = "config.yml"
_reserved_keys = ["load", "log"]


def _save(model_dir):
    import os, yaml

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    config_yml = yaml.dump(_dict(), default_flow_style=False)
    with open(os.path.join(model_dir, _config_file_name), "w+") as f:
        f.write(config_yml)


def _add(key, value, create=True):
    import logging
    if key.startswith("_"):
        raise ValueError("The config key {} starting with '_' is invalid.".format(key))
    if key in _reserved_keys:
        raise ValueError("The config key {} is reserved.".format(key))
    g = globals()
    if key in g:
        value = type(g[key])(value)
        if g[key] != value:
            logging.info("The original value of '{}' is '{}', but it'll be set to '{}'.".format(key, g[key], value))
    elif not create:
        raise ValueError("{} is unknown configuration key.".format(key))
    g[key] = value


def _dict():
    return {k: v for k, v in globals().items()
            if not k.startswith("_") and k not in _reserved_keys}


def log():
    import logging
    logging.info("------------------- All configurations --------------------")
    kv = _dict()
    for k in sorted(kv.keys()):
        logging.info("%s = %s", k, kv[k])
    logging.info("------------------------------------------------------------")


def load(model_dir, configs, initialize=False):
    import os, yaml

    saved_config_file = os.path.join(model_dir, _config_file_name)
    if os.path.exists(saved_config_file):
        configs = [saved_config_file] + configs
    elif not initialize:
        raise ValueError("{} is an invalid model directory.".format(model_dir))

    for cfg in configs:
        kv = [s.strip() for s in cfg.split("=", 1)]
        if len(kv) == 1:
            if not os.path.exists(cfg):
                raise ValueError("The configuration file {} doesn't exist.".format(cfg))
            obj = yaml.load(open(cfg).read())
            for k, v in obj.items():
                # The type of value was already determined by YAML.
                _add(k, v)
        else:
            # The value whose type was already determined by YAML can be added.
            _add(*kv, create=False)

    if not os.path.exists(saved_config_file) and initialize:
        _save(model_dir)
