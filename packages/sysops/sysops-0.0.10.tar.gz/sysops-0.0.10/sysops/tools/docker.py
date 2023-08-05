#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Docker(object):
    @staticmethod
    def login(ctx, username, password, reg=None):
        cmd = 'docker login -u ' + username + ' -p ' + password
        if reg is not None:
            cmd += ' ' + reg
        ctx.sudo(cmd)
