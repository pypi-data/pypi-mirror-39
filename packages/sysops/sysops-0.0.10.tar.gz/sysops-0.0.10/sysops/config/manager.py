#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from invoke import Config as InvCfg, Context as InvCtx


def _config_merge(default, host):
    for key in host:
        if key not in default:
            default[key] = host[key]
        else:
            if isinstance(host[key], str):
                default[key] = host[key]
            else:
                _config_merge(default[key], host[key])
    return default


class Host:

    def __init__(self, config):
        """Constructor"""
        self._data = {}
        if 'host' in config:
            self._data['host'] = config['host']
        if 'domain' in config:
            self._data['domain'] = config['domain']
        if 'port' in config:
            self._data['port'] = config['port']
        if 'os' in config:
            self._data['os'] = config['os']
        if 'mirror' in config:
            self._data['mirror'] = config['mirror']
        if 'username' in config:
            self._data['username'] = config['username']
        if 'fullname' in config:
            self._data['fullname'] = config['fullname']
        if 'users' in config:
            self._data['users'] = {}
            users = config['users']
            for item in users:
                user = users[item]
                self._data['users'][item] = dict(key=user['key'], password=user['password'])

    @property
    def data(self):
        return self._data

    @property
    def host(self):
        return self._data['host']

    @property
    def domain(self):
        return self._data['domain']

    @property
    def fqdn(self):
        return self.host + '.' + self.domain

    @property
    def port(self):
        return self._data['port']

    @property
    def os(self):
        return self._data['os']

    @property
    def mirror(self):
        return self._data['mirror']

    @property
    def username(self):
        return self._data['username']

    @property
    def fullname(self):
        return self._data['fullname']

    @property
    def users(self):
        return self._data['users']


def singleton(cls):
    _instances = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]

    return _singleton


@singleton
class Config(object):

    def __init__(self, ctx=None):
        self._hosts = {}
        if ctx is None:
            cfg = InvCfg(project_location="./configs")
            cfg.load_project()
            self._context = InvCtx(cfg)
        else:
            self._context = ctx

        hosts = self.config.Hosts
        default = hosts['default']
        for key in hosts:
            if key == 'default':
                continue
            host = Host(_config_merge(dict(default), dict(hosts[key])))
            self._hosts[key] = host

    @property
    def hosts(self):
        return self._hosts

    @property
    def context(self):
        return self._context

    @property
    def config(self):
        return self.context.config
