#coding:utf-8

import jieba
import jieba.posseg as pseg
import mysql.connector
from mysql.connector import errorcode

def to_bytestring(s, enc='utf-8'):
	"""convert the given unicode string to a bytestring, using the standard encoding,
	unless it's already a bytestring"""
	if s:
		if isinstance(s, str):
			return s
		else:
			return s.encode(enc)

def DBOp(fn, **kwargs):
	cursors = []
	try:
		result = None
		cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='saif')

		cursors, result = fn(cnx, **kwargs)

		cnx.commit()

	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	finally:
		if len(cursors) > 0:
			for cursor in cursors:
				cursor.close()
		cnx.close()
		return result
	

def _report_analysis(cnx):
	PROCESS_STEP = 1
	MAXITEMS = 20
	cursors = []
	result = None

	cursor_q = cnx.cursor()
	cursors.append(cursor_q)
	cursor_u = cnx.cursor(buffered = True)
	cursors.append(cursor_u)
	cursor_i = cnx.cursor(buffered = True)
	cursors.append(cursor_i)

	cursor_q.execute("SELECT symbol, year, article FROM report WHERE process_step <> 1 OR process_step IS NULL LIMIT 1")
	row = cursor_q.fetchone()
	print "row: "
	print (row)
	"""
	while row is not None:
		print (row)
		row = cursor_q.fetchone()
	"""

	"""

	while True:

		cursor_q = cnx.cursor()
		cursors.append(cursor_q)
		cursor_u = cnx.cursor(buffered = True)
		cursors.append(cursor_u)
		cursor_i = cnx.cursor(buffered = True)
		cursors.append(cursor_i)



		retrieve_to_process = ("SELECT symbol, year, article FROM report "
			" WHERE process_step <> %s OR process_step IS NULL")

		completion_update = ("UPDATE report SET process_step = %S"
			"WHERE symbol = %s AND year = %s")


		cursor_q.execute(retrieve_to_process, (PROCESS_STEP))


		
		if sum(1 for e in cursor_q) == 0 : #finish all the analysis and return
			break
		

		for (symbol, year, article) in cursor_q:
			print symbol
			print year
			print article
			print '\n'

			cuts = pseg.cut(article)
			for word, flag in cuts:
				print word + ' / ' + flag
		"""

	return (cursors, result)



if __name__ == '__main__' :
	DBOp(_report_analysis)
