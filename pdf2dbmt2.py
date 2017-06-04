# coding=utf-8
import os
import time
import pdfa
import shutil
import logging
import threading
import mysql.connector
import MySQLdb

from mysql.connector import errorcode
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.psparser import PSException
from pdfminer.pdfparser import PSEOF

import jieba
import jieba.posseg as pseg


def _create_folder(path, postfix):
	folder_name = path.split("\\")[-1] + postfix
	folder_path = os.path.abspath(os.path.join(os.path.join(path, os.pardir), folder_name))
	if False == os.path.exists(folder_path):
		os.makedirs(folder_path)
	return folder_path

def creat_broken_folder(path):
	return _create_folder(path, "_b")

def creat_unextract_folder(path):
	return _create_folder(path, "_u")

def creat_compeletion_folder(path):
	return _create_folder(path, "_c")

class pdf2DBThread(threading.Thread):
	def __init__(self, pdf):
		# format path, remove the last tail '\\'
		if pdf.split("\\")[-1] == '':
			pdf = pdf[:-1]
		threading.Thread.__init__(self)
		self.pdf = pdf 

	def run(self):
		itr(self.pdf, lexAnalysisSaveToDB)


def itr(folder, fn):
	print "itr"

	"""iterate all the pdf files, save to DB. In order to continue where broken, compelete files will be removed to completion folder"""
	completeFolder = creat_compeletion_folder(folder)
	brokenFolder = creat_broken_folder(folder)
	unextractFolder = creat_unextract_folder(folder)

	bk_file = brokenFolder+'\\bk.txt' # use bk_file later to re download the report files
	un_file = unextractFolder+"\\unextract.txt" # un_file records the PDF files could not extract text, may research new method to do it later

	for root, dirs, files in os.walk(folder):
		unextact_list = []
		broken_list = []

		for file in files:
			print file
			try:
				sentences = 0
				words = 0
				avgwords = 0.0

				x = file.split('_')
				code = x[0]
				year = x[1]

				# may raise PDFTextExtractionNotAllowed
				text_content = pdfa.get_pages(os.path.join(root, file))

				sentences, words, avgwords = simpleStat(text_content)
				
				# may raise IOError, DBException
				if fn(code, year, text_content, avgwords, sentences, words) == True:
					shutil.move(root+"\\"+file, completeFolder)
					print "Success: " + root+file
				else:
					print "Fail1: " + root+file

			# occurs once PDF could not open, file maybe damaged during the downloading
			except (PDFSyntaxError, PSEOF) as e:
				print "Fail: " + file
				print e
				broken_list.append(file)
				with open(bk_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, brokenFolder)
				except Exception, e:
					print Exception, ":", e

			# occurs when text could not extracted from PDF
			except (PDFTextExtractionNotAllowed, Exception) as e:
				print "Fail: " + file
				print e
				unextact_list.append(file)
				with open(un_file, 'a') as infile:
					infile.write(file)
					infile.write('\n')
				try:
					shutil.move(root+"\\"+file, unextractFolder)
				except Exception, e:
					print Exception, ":", e

def simpleStat(article):
	sentences = 0
	words = 0
	avgwords = 0.0
	sentences = article.count('。') 
	words = len(article.strip())
	# average
	if sentences != 0:
		avgwords = words / sentences
	else:
		avgwords = 0.0

	return (sentences, words, avgwords)

def saveToDB(symbol, year, article, avgwords, sentences, words):
	try:
		cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='saif')
		cursor = cnx.cursor()

		add_report = ("INSERT INTO report "
			"(symbol, year, article, avgwords, sentences, words) "
			"VALUE (%s, %s, %s, %s, %s, %s) ")
		data_report = (symbol, year, article, avgwords, sentences, words)

		cursor.execute(add_report, data_report)

		cnx.commit()
		return True

	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor.close()
		cnx.close()
		return None
	finally:
		if cursor != None:
			cursor.close()
		if cnx != None:
			cnx.close()

def lexAnalysisSaveToDB(symbol, year, article, avgwords, sentences, words):
	print "lexAnalysisSaveToDB"
	CURRENT_STEP = 1
	d = {}
	insertion = []
	n = 0
	process_step = 0
	result = None
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saif", charset = "utf8")
		c = db.cursor()

		cuts = pseg.cut(article.strip())

		for word, flag in cuts:
			if flag != 'x' and flag != 'm' and flag != 'uj': # filter out meaningless cut
				if word in d:
					d[word][1] += 1
				else:
					d[word] = [flag, 1]

		for k in d:
			insertion.append( (k, d[k][0], symbol, year, d[k][1]) )

		ins_ws = """INSERT INTO wordstatistic (word, cha1, symbol, year, amt) VALUES (%s, %s, %s, %s, %s) """

		n = 0
		n = c.executemany(ins_ws, insertion)
		print n

		if n == 0:
			process_step = 0 # todo: 0. will update later, by nlp2.py, start manually 1. will stop process
		else:
			process_step = CURRENT_STEP

		ins_rpt = """INSERT INTO report (symbol, year, article, avgwords, sentences, words, process_step) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

		n = 0
		n = c.execute(ins_rpt, (symbol, year, article, avgwords, sentences, words, process_step))
		print n
		if n == 0: # update is not success
			print "_fail to insert new record to table report, and start rollback"
			raise MySQLdb.Error("_fail to insert new record to table report, and start rollback")
		else:
			result = True
	except MySQLdb.Error, e:
		print MySQLdb.Error, ":", e
		db.rollback()
		raise
	except Exception, e:
		print Exception, ":", e
	finally:
		db.commit()
		return result


if __name__ == '__main__':
	test = pdf2DBThread("C:\\_workshop\\prj_saif_paper\\pdfs\\test")
	test.start()




