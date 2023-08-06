# coding: utf8
"""
WARNING: a monkeypatch-on-import wrapper of `pd_streamlib`.
"""

from __future__ import print_function, unicode_literals, absolute_import, division

from . import pd_streamlib
pd_streamlib.patch_all()
