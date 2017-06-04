from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.converter import PDFPageAggregator

def with_pdf(pdf_doc, pdf_pwd, fn, *args):
	result = None
	fp = None
	
	with open(pdf_doc, 'rb') as fp:
		# open pdf file
		#fp = open(pdf_doc, 'rb')
		# create a parser object associated with the file object
		parser = PDFParser(fp)
		# create a PDFDocument object that stores the document structure
		#doc = PDFDocument()
		doc = PDFDocument(parser)
		# connect the parser and document objects
		parser.set_document(doc)
		#doc.set_parser(parser)
		# supply the password for initialization
		#doc.initialize(pdf_pwd)

		if doc.is_extractable:
			# apply the function and return the result
			result = fn(doc, *args)
			return result
		else: 
			raise PDFTextExtractionNotAllowed


def _parse_pages (doc):
	"""with an open PDFDocument object, get the pages and parse each one"""
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)

	text_content = []
	#for i, page in enumerate(doc.get_pages()):
	for i, page in enumerate(PDFPage.create_pages(doc)):
		interpreter.process_page(page)
		layout = device.get_result()
		text_content.append(parse_lt_objs(layout._objs, (i+1)))

	return text_content

def parse_lt_objs(lt_objs, page_number, text=[]):
	text_content = []
	page_text = {}

	for lt_obj in lt_objs:
		if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
			page_text = update_page_text_hash(page_text, lt_obj)
			#text_content.append(lt_obj.get_text())
		elif isinstance(lt_obj, LTFigure):
			text_content.append(parse_lt_objs(lt_obj._objs, page_number, text_content))
	for k, v in sorted([(key, value) for (key, value) in page_text.items()]):
		text_content.append('\n'.join(v))

	return '\n'.join(text_content)

def to_bytestring(s, enc='utf-8'):
	"""convert the given unicode string to a bytestring, using the standard encoding,
	unless it's already a bytestring"""
	if s:
		if isinstance(s, str):
			return s
		else:
			return s.encode(enc)

def update_page_text_hash(h, lt_obj, pct=0.25):
	"""Use the bbox x0, x1 values within pct% to produce lists of associated text within the hash"""
	x0 = lt_obj.bbox[0]
	x1 = lt_obj.bbox[2]
	key_found = False
	for k, v in h.items():
		hash_x0 = k[0]
		if x0 >= (hash_x0 * (1.0-pct)) and (hash_x0 * (1.0+pct)) >= x0:
			hash_x1 = k[1]
			if x1 >= (hash_x1 * (1.0-pct)) and (hash_x1 * (1.0+pct)) >= x1:
				key_found = True
				v.append(to_bytestring(lt_obj.get_text()))
				h[k] = v
	if not key_found:
		h[(x0, x1)] = [to_bytestring(lt_obj.get_text())]
	return h


def get_pages (pdf_doc, pdf_pwd=''):
	content = with_pdf(pdf_doc, pdf_pwd, _parse_pages)
	if content != None:
		return '\n\n'.join( content )
	else:
		return None

if __name__ == '__main__':
	pdf_name = "601318_2014_1200719857.PDF"
	get_pages(pdf_name)