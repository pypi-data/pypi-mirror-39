#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import makedirs
from os.path import dirname, exists, isfile


def sudo(ctx, path, command):
    cmd = 'bash -c "cd ' + path + ' && '
    cmd += command
    cmd += '"'
    ctx.sudo(cmd)


def mkdir(path, f=False):
    if not f and exists(path) and isfile(path):
        f = True
    if f:
        path = dirname(path)
    if not exists(path):
        makedirs(path)


def read_text(path):
    with open(path, 'r') as f:
        text = f.read()
    return text


def write_text(text, path):
    mkdir(path, True)
    with open(path, 'w') as f:
        f.write(text)
