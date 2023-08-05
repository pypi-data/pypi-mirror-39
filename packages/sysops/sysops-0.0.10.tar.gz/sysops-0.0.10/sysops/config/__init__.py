#!/usr/bin/env python
# -*- coding: utf-8 -*-
# sysops/config

from os.path import join as path_join
from os.path import sep as path_sep

from .manager import Config, Host

CONF_PATH = path_join(".", "configs")
CONF_APT_PATH = path_join(CONF_PATH, "apt")
CONF_PRESEED_PATH = path_join(CONF_PATH, "boot")

BUILD_PATH = path_join(".", "build")
BUILD_TMP_PATH = path_join(BUILD_PATH, "temp")

DOCKER_PATH = path_join(".", "build", "docker")
CFG_WEB_PATH = path_join(DOCKER_PATH, "cfg-web")

SH_PATH = "." + path_sep + "scripts"
