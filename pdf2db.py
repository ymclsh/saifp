import pdfa
import mysql.connector
from mysql.connector import errorcode
import logging
import os
import shutil


def itr(folder, fn):
	"""iterate all the pdf files, save to DB. In order to continue where broken, compelete files will be removed to completion folder"""
	for root, dirs, files in os.walk(folder):
		completeFolder = root+"completion"
		brokenFolder = root+"broken"

		if False == os.path.exists(completeFolder):
			os.makedirs(completeFolder)

		for file in files:
			try:
				sentences = 0
				words = 0
				avgwords = 0.0

				x = file.split('_')
				code = x[0]
				year = x[1]
				text_content = pdfa.get_pages(os.path.join(root, file))
				if text_content != None:
					sentences = text_content.count('。') 
					words = len(text_content)
					if sentences != 0:
						avgwords = words / sentences
					else:
						avgwords = 0.0

					if fn(code, year, text_content, avgwords, sentences, words) == True:
						shutil.move(root+file, completeFolder)
						print "Success: " + root+file
					else:
						print "Fail: " + root + file
				else:
					print "Fail:" + root + file
			except Exception, e:
				print "Fail: "+ root+file
				print Exception, ":", e
				shutil.move(root+file, brokenFolder)


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


"""

def DBOp(fn, **kwargs):
	try:
		result = None
		cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='saif')
		cursor = cnx.cursor()

		result = fn(cursor, **kwargs)

		cnx.commit()

		return result

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


def _update_blank_statistics(cursor, avgwords, sentences, words):
	query = ("SELECT symbol, year, article, avgwrods, sentences, words FROM report "
		"WHERE article != '' AND sentences IS NULL")

"""

if __name__ == '__main__':
	itr("C:\\_private\\saif\\paper\\all\\zip\\2015\\download\\2014_full\\", saveToDB)




