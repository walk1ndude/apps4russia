# -*- coding: utf-8 -*-
__author__ = 'walkindude'

#from pdfminer.pdfparser import PDFParser
#from pdfminer.pdfdocument import PDFDocument
#from pdfminer.pdfpage import PDFPage
#from pdfminer.pdfpage import PDFTextExtractionNotAllowed
#from pdfminer.pdfinterp import PDFResourceManager
#from pdfminer.pdfinterp import PDFPageInterpreter
#from pdfminer.pdfdevice import PDFDevice

from StringIO import StringIO

import re

from python_glr_parser.glr_runner import run_glr

try:
	from xml.etree.cElementTree import XML
except ImportError:
	from xml.etree.ElementTree import XML
import zipfile

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'

def preprocess_paragprahs(paragraphs):
	i = 0
	while i != len(paragraphs) - 2:
		firstP, secondP = paragraphs[i], paragraphs[i + 1]
		#параграф начинается не с заглавной буквы, то ищем первый знак препинания в данном параграфе и все
		#что до него и его включаем в предыдущий параграф
 		if not secondP[0].isupper():
			m = re.search(r'[!.?]', secondP)
			if m:
				paragraphs[i] = ''.join((firstP, secondP[:m.end(0)]))
				paragraphs[i + 1] = secondP[m.end(0):]
				i += 1
			else:
				paragraphs[i] = ''.join((firstP, secondP))
				paragraphs.pop(i + 1)
		else:
			i += 1



def parse_docx(file):
	"""
	Take the path of a docx file as argument, return the text in unicode.
	"""
	document = zipfile.ZipFile(file)
	xml_content = document.read('word/document.xml')
	document.close()
	tree = XML(xml_content)

	parsed_paragraphs = []
	pars = []
	for paragraph in tree.getiterator(PARA):
		par=([node.text
				 for node in paragraph.getiterator(TEXT)
				 if node.text])
		curPar = ''.join(par)
		if curPar:
			pars.append(curPar)

	if pars:
		preprocess_paragprahs(pars)

		print pars

		parsed_paragraphs.append(run_glr(''.join(tuple(pars))))

	return parsed_paragraphs


# def parse_pdf(file):
# 	fp = open(file, 'rb')
# 	# Create a PDF parser object associated with the file object.
# 	parser = PDFParser(fp)
# 	# Create a PDF document object that stores the document structure.
# 	# Supply the password for initialization.
# 	document = PDFDocument(parser)
# 	# Check if the document allows text extraction. If not, abort.
# 	if not document.is_extractable:
# 		raise PDFTextExtractionNotAllowed
# 	# Create a PDF resource manager object that stores shared resources.
# 	rsrcmgr = PDFResourceManager()
# 	# Create a PDF device object.
# 	device = PDFDevice(rsrcmgr)
# 	retstr = StringIO()
# 	# Create a PDF interpreter object.
# 	interpreter = PDFPageInterpreter(rsrcmgr, device)
# 	# Process each page contained in the document.
# 	for page in PDFPage.create_pages(document):
# 		interpreter.process_page(page)
# 		data = retstr.getvalue()
#
# 	print data