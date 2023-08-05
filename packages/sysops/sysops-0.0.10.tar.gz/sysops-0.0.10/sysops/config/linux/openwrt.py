#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .linux import Linux


class Openwrt(Linux):

    def install_ss(self):
        self.run("cd ~")
        url = "http://openwrt-dist.sourceforge.net/packages/openwrt-dist.pub"
        self.run("wget " + url)
        self.run("opkg-key add openwrt-dist.pub")
        self.run("rm openwrt-dist.pub")
        arch = self.run("opkg print-architecture | awk '{print $2}'")
        arch = "x86_64"
        file = "/etc/opkg/customfeeds.conf"
        url = "http://openwrt-dist.sourceforge.net/packages/LEDE"
        text = "src/gz openwrt_dist "
        text += url + "/base/" + arch
        self.run("echo text >> " + file)
        text = "src/gz openwrt_dist_luci "
        text += url + "/luci"
        self.run("echo text >> " + file)
        self.run("opkg update")
        self.install("ChinaDNS luci-app-chinadns")
        self.install("dns-forwarder luci-app-dns-forwarder")
        # self.install("shadowsocks-libev-mbedtls luci-app-shadowsocks")
        self.install("shadowsocks-libev luci-app-shadowsocks")
        # self.install("ShadowVPN luci-app-shadowvpn")
