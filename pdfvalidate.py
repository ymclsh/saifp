import pdfa
import os
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.psparser import PSException
from pdfminer.pdfparser import PSEOF

import shutil

def valid(path):
	broken_folder_name = path.split("\\")[-1] + "_broken"
	unextractable_folder_name = path.split("\\")[-1] + "_unextractable"

	unextact_path = os.path.abspath(os.path.join(os.path.join(path, os.pardir), unextractable_folder_name))
	broken_path = os.path.abspath(os.path.join(os.path.join(path, os.pardir), broken_folder_name))

	bk_file = broken_path+'\\bk.txt'
	unextract_file = unextact_path+"\\unextract.txt"

	if False == os.path.exists(broken_path):
		os.makedirs(broken_path)
	if False == os.path.exists(unextact_path):
		os.makedirs(unextact_path)

	for root, dirs, files in os.walk(path):
		unextact_list = []
		broken_list = []
		for file in files:
			print file
			try:
				pdfa.get_pages(os.path.join(root, file))
				
			except PDFTextExtractionNotAllowed, e:
				print "Fail: " + file
				print PDFTextExtractionNotAllowed, ":", e
				unextact_list.append(file)
				with open(unextract_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, unextact_path)
				except Exception, e:
					print Exception, ":", e

			except PDFSyntaxError, e:
				print "Fail: " + file
				print PDFSyntaxError, ":", e
				broken_list.append(file)
				with open(bk_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, broken_path)
				except Exception, e:
					print Exception, ":", e

			except PSEOF, e:
				print "Fail: " + file
				print PSEOF, ":", e
				broken_list.append(file)
				with open(bk_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, broken_path)
				except Exception, e:
					print Exception, ":", e

			except Exception, e:
				print "Fail: " + file
				print Exception, ":", e
				unextact_list.append(file)
				with open(unextract_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, unextact_path)
				except Exception, e:
					print Exception, ":", e				
"""
		with open(bk_file, 'w') as infile:
			for file in broken_list:
				infile.write(file)
				infile.write('\n')
				try:
					shutil.move(root+"\\"+file, broken_path)
				except Exception, e:
					print Exception, ":", e
		with open(unextract_file, 'w') as infile:
			for file in unextact_list:
				infile.write(file)
				infile.write('\n')
				try:
					shutil.move(root+"\\"+file, unextact_path)
				except Exception, e:
					print Exception, ":", e"""


if __name__ == '__main__':
	valid("C:\\_workshop\\prj_saif_paper\\pdfs\\2014_full")


