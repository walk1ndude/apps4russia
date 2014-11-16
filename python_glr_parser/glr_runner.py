# -*- coding: utf-8 -*-
from glr import GLRParser

dictionaries_implementer = {
    u"IMPL": [u"исполнитель", u"Исполнитель"],
}

dictionaries_customer = {
    u"CUST": [u"заказчик", u"Заказчик"],
}


grammar_impl = u"""
    S = IMPL
"""

grammar_cust = u"""
    S = CUST
"""


def run_glr(text):
	glr = GLRParser(grammar_impl, dictionaries=dictionaries_implementer, debug=False)
	result_impl= glr.parse(text)

	glr = GLRParser(grammar_cust, dictionaries=dictionaries_customer, debug=False)
	result_cust= glr.parse(text)

	return (result_impl, result_cust)
