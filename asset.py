#coding:utf8
import MySQLdb

def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		con = db.cursor()

		con.execute("""SELECT * FROM asset_tmp""")

		insert = []
		dummy = 0.00
		for row in con.fetchall():
			for i in range(11):
				if i <= 9:
					insert.append( (row[0], 2005+i, row[i+1], row[i+2]) )
				else:
					insert.append( (row[0], 2005+i, row[i+1], dummy) )

		ins = """INSERT INTO asset (symbol, year, asset, assetp1) VALUES (%s, %s, %s, %s)"""
		#print insert[32900:32950]
		n = con.executemany(ins, insert)
		print n
		db.commit()
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		db.close()


if __name__ == '__main__' :
	itr()