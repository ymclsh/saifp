#coding:utf8
import MySQLdb

def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		con = db.cursor()

		con.execute("""SELECT * FROM rev_tmp""")

		insert = []
		for row in con.fetchall():
			if row[0] == "000001.SZ":
				print row
			for i in range(11):
				insert.append( (row[0].split('.')[0].replace(u'\ufeff',''), 2005+i, row[i+18], row[i+4]) )

		ins = """INSERT INTO earning (symbol, year, rev, pft) VALUES (%s, %s, %s, %s)"""
		#print insert[32900:32950]
		con.executemany(ins, insert)
		db.commit()
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		db.close()


if __name__ == '__main__' :
	itr()