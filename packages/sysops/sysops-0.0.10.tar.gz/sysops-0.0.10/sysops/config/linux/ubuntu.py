#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .deblike import deblike


@deblike
class Ubuntu(object):

    @staticmethod
    def gen_preseed_conf(values, write=False, dst_path=None):
        cfg_dst = Ubuntu.gen_preseed('ubuntu', values, write, dst_path)
        return cfg_dst

    @staticmethod
    def gen_apt_src(mirror=None, dir_main='ubuntu', dir_sec='ubuntu-security',
                    version=None, universe=True, restricted=True,
                    backports=False, src=True, write=False, dst_path=None):
        if mirror is None:
            mirror = Ubuntu.MIRRORS['auto']
        elif '.' not in mirror:
            mirror = Ubuntu.MIRRORS[mirror]
        if version is None:
            version = 18
        repotype = Ubuntu.REPO_TYPES
        if not universe:
            repotype.remove('universe')
        if not restricted:
            repotype.remove('restricted')
        values = dict(
            mirror=mirror, dir_main=dir_main, dir_sec=dir_sec,
            version=Ubuntu.VERSIONS[version],
            repotype=' '.join(repotype),
        )
        return Ubuntu.gen_src_list(values, backports, src, write, dst_path)


Ubuntu.VERSIONS = {
    18: 'bionic',
    16: 'xenial',
}

Ubuntu.MIRRORS.update({
    'cn': 'cn.archive.ubuntu.com',
    'hk': 'hk.archive.ubuntu.com',
    'sg': 'sg.archive.ubuntu.com',
    'kr': 'kr.archive.ubuntu.com',
    'jp': 'jp.archive.ubuntu.com',
    'tw': 'tw.archive.ubuntu.com',
    'us': 'us.archive.ubuntu.com',
    'sec': 'security.ubuntu.com',
    'auto': 'archive.ubuntu.com',
})

Ubuntu.REPO_TYPES = ['main', 'universe', 'restricted', 'multiverse']
