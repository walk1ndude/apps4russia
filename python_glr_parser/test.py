#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'gmdidro'
from glr import GLRParser

dictionaries = {
    u"CLOTHES": [u"куртка", u"пальто", u"шубы"]
}

grammar = u"""
    S = adj<agr-gnc=1> CLOTHES
"""

glr = GLRParser(grammar, dictionaries=dictionaries)

text = u"на вешалке висят. пять красивых курток. и вонючая шуба"
for parsed in glr.parse(text):
    print "FOUND:", parsed