# -*- coding: utf-8 -*-
from glr import GLRParser

dictionaries = {
    u"CLOTHES": [u"куртка", u"пальто", u"шубы"]
}

grammar = u"""
    S = adj<agr-gnc=1> CLOTHES
"""

def run_glr(text, grammar=grammar, dictionaries=dictionaries):
	glr = GLRParser(grammar, dictionaries=dictionaries, debug=False)

	result = []

	for parsed in glr.parse(text):
		result.append(parsed)

	return result
