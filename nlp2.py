#coding:utf-8

import jieba
import jieba.posseg as pseg
import MySQLdb
import time


def to_bytestring(s, enc='utf-8'):
	"""convert the given unicode string to a bytestring, using the standard encoding,
	unless it's already a bytestring"""
	if s:
		if isinstance(s, str):
			return s
		else:
			return s.encode(enc)

def lexAnalysis():
	pass


def reportAnalysisDB():
	CURRENT_STEP = 1
	MAX_RETURN = 10
	d = {}
	insert = []

	db = MySQLdb.connect(host = "localhost", user = "root", db = "saif", charset = "utf8")

	c = db.cursor()

	try:
		while True:
			try:
				start = time.time() # for cauculating time comusme, will be removed in production release

				n = 0 # initialize n for select
				n = c.execute("""SELECT symbol, year, article FROM report WHERE process_step <> %s OR process_step IS NULL LIMIT %s""", (CURRENT_STEP, MAX_RETURN))
				if n == 0: # all items are finished
					break
				for row in c.fetchall():

					# initialize d, insert for new round process
					d = {}
					insert = []

					cuts = pseg.cut(row[2].strip()) # lex analysis

					for word, flag in cuts:
						if flag != 'x' and flag != 'm' and flag != 'uj': # filter out meaningless cut
							if word in d:
								d[word][1] += 1
							else:
								d[word] = [flag, 1]

					for k in d:
						insert.append( (k, d[k][0], row[0], row[1], d[k][1]) )

					q = """INSERT INTO wordstatistic (word, cha1, symbol, year, amt) VALUES (%s, %s, %s, %s, %s) """

					c.executemany(q, insert)

					u = """UPDATE report SET process_step = %s WHERE symbol = %s AND year = %s"""
					n = 0 # initialize n for update
					n = c.execute(u, (CURRENT_STEP, row[0], row[1]))
					if n == 0: # if update is not success
						db.rollback()

				print ("--- %s seconds ---" % (time.time() - start))
			except MySQLdb.Error, e:
	    		print 'Error %d: %s' % (e.args[0], e.args[1])
			finally:
				db.commit()
	except MySQLdb.Error, e:
	    print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		if db:
			db.close()
	
	



if __name__ == '__main__' :
	reportAnalysisDB()