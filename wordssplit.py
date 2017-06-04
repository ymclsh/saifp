#coding:utf-8

import MySQLdb


def itr():
	db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
	c = db.cursor()

	try:

		for i in range(2014, 2016):
			tablename = "words_" + str(i)
			print tablename
			n = 0
			n = c.execute("""SELECT word, cha1, cha2, cha3, cha4, cha5, symbol, year, amt FROM wordstatistic WHERE year = %s""", (str(i), ))

			ins = """INSERT INTO """ + tablename + """ (word, cha1, cha2, cha3, cha4, cha5, symbol, year ,amt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
			for row in c.fetchall():
				c.execute(ins, row)
			db.commit()

						
			#n = 0
			#ins = """INSERT INTO """ + tablename + """ (word, cha1, cha2, cha3, cha4, cha5, symbol, year ,amt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""" 
			"""print ins
			n = c.executemany(ins, insert)
			print n
			db.commit()"""
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
		#db.rollback()
	finally:
		db.close()



if __name__ == '__main__' :
	itr()