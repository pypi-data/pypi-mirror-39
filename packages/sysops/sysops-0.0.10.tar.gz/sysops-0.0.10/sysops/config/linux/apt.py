#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import Template

from .. import path_join, path_sep, CONF_APT_PATH, BUILD_TMP_PATH
from ..util import write_text, read_text


def apt_gen(cls):
    mirrors = {
        '163': 'mirrors.163.com',
        'aly': 'mirrors.aliyun.com',
        'aly-vpc': 'mirrors.cloud.aliyuncs.com',
        'xtom': 'mirror.xtom.com.hk',
        'sggs': 'mirror.sg.gs',
        # kr
        'harukasan': 'ftp.harukasan.org',
        # us
        'steadfast': 'mirror.steadfast.net',
    }
    repo_types = []

    def gen_src_list(values, backports, src, write=False, dst_path=None):
        src_path = path_join(CONF_APT_PATH, 'sources.list')
        cfg_src = read_text(src_path)
        cfg_dst = Template(cfg_src).safe_substitute(values)
        lines = cfg_dst.splitlines()
        dst = list(lines)
        for line in lines:
            if not backports and line.find('backports') != -1:
                dst.remove(line)
            if not src and line.find('deb-src') != -1:
                dst.remove(line)
        cfg_dst = "\n".join(dst) + "\n"
        if write:
            base_path = path_join(BUILD_TMP_PATH, 'apt', 'sources.list.')
            if dst_path is None:
                dst_path = path_join(base_path + values['dir_main'])
            elif path_sep not in dst_path:
                dst_path = path_join(base_path + dst_path)
            write_text(cfg_dst, dst_path)
        return cfg_dst

    cls.MIRRORS = mirrors
    cls.REPO_TYPES = repo_types
    cls.gen_src_list = staticmethod(gen_src_list)

    return cls
