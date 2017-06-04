#coding:utf-8
import MySQLdb


def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		c = db.cursor()
		n = 0
		n = c.execute("""SELECT symbol, year, dur FROM soip""")
		print n
		soiplist = []
		for row in c.fetchall():
			for delta in range(row[2]):
				x = [row[0], str(int(row[1])+delta)] 
				if x not in soiplist:
					soiplist.append(x)
		c.executemany("""INSERT INTO soip_idx (symbol, year) VALUES (%s, %s)""", soiplist)
		db.commit()

	except MySQLdb.Error, e:
		print e
		db.rollback()
	finally:
		if c:
			c.close()
		if db:
			db.close()

if __name__ == '__main__':
	itr()