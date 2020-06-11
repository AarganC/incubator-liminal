#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os

DEFAULT_DAGS_ZIP_NAME = 'rainbows.zip'
DEFAULT_RAINBOW_HOME = os.path.expanduser('~/rainbow_home')
DEFAULT_RAINBOWS_SUBDIR = "rainbows"
RAINBOW_HOME_PARAM_NAME = "RAINBOW_HOME"


def get_rainbow_home():
    if not os.environ.get(RAINBOW_HOME_PARAM_NAME):
        print("no environment parameter called RAINBOW_HOME detected")
        print(f"registering {DEFAULT_RAINBOW_HOME} as the RAINBOW_HOME directory")
        os.environ[RAINBOW_HOME_PARAM_NAME] = DEFAULT_RAINBOW_HOME
    return os.environ.get(RAINBOW_HOME_PARAM_NAME, DEFAULT_RAINBOW_HOME)


def get_dags_dir():
    # if we are inside airflow, we will take it from the configured dags folder
    base_dir = os.environ.get("AIRFLOW__CORE__DAGS_FOLDER", get_rainbow_home())
    return os.path.join(base_dir, DEFAULT_RAINBOWS_SUBDIR)
