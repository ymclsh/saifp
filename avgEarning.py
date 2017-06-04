#coding:utf-8
import MySQLdb

def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		c = db.cursor()
		n = c.execute("""SELECT symbol, avg(rev), avg(pft) FROM saifp.earning WHERE rev != 0 AND pft != 0 GROUP BY symbol ORDER BY symbol DESC""")
		n = 0
		avgEarning = c.fetchall()

		for avg in avgEarning:
			n = c.execute("""UPDATE earning SET rev_avg = %s, pft_avg = %s WHERE symbol = %s AND rev_avg IS NULL""", (avg[1], avg[2], avg[0]))
			print n
		#	n = c.execute("""SELECT symbol, year, revp1, pftp1 FROM saifp.earning WHERE revp1 != 0 AND symbol = %s""", (avg[0], ))
		#	for earn in c.fetchall():
		#		rev_avg_rate = earn[2] / avg[1]
		#		pft_avg_rate = earn[3] / avg[2]
		#		c.execute("""UPDATE earning SET rev_avg = %s, pft_avg = %s, rev_avg_rate = %s, pft_avg_rate = %s WHERE symbol = %s AND year = %s""", (avg[1], avg[2], rev_avg_rate, pft_avg_rate, earn[0], earn[1]))

		db.commit()
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		if db:
			db.close()

if __name__ == '__main__':
	itr()