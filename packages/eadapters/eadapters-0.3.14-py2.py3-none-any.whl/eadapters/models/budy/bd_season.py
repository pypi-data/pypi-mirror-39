#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import bd_common

from .. import season

class BDSeason(season.ESeason, bd_common.BDCommon):
    pass
