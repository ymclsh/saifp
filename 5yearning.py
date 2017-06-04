#coding:utf-8
import MySQLdb

def itr():

	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		c = db.cursor()

		#just for testing LIMIT 10
		c.execute("""SELECT symbol, year, rev, pft FROM earning ORDER BY symbol, year DESC""") # handle the latest first, older later
		pre_symbol = 0
		update = [] # symbol, year, rev, pft, revp1, pftp1, revp2, pftp2, revp3, pftp3, revp4, pftp4, revp5, pftp5
		u = [] # revp1, pftp1, revp2, pftp2, revp3, pftp3, revp4, pftp4, revp5, pftp5
		usql = """UPDATE earning SET revp1 = %s, pftp1 = %s, revp2 = %s, pftp2 = %s, revp3 = %s, pftp3 = %s, revp4 = %s, pftp4 = %s, revp5 = %s, pftp5 = %s WHERE symbol = %s AND year = %s"""

		for row in c.fetchall():

			if pre_symbol == 0 or pre_symbol != row[0] : #start to handle for new company
				pre_symbol = row[0]
				update = []
				update.append(list(row) + [ 0 for i in range(10)])
			else:

				pre_node = update[-1]

				last_year = pre_node[1]
				current_year = row[1]
				diff = gap(last_year, current_year)

				u = [0 for i in range(10)]

				for i in range(10 - 2*(diff-1)):
					u[2*(diff - 1) + i] = pre_node[2 + i]

				update.append(list(row) + u)
				n = c.execute(usql, (u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],row[0], row[1]))
				print row[0]
				print row[1]
				print n 
				db.commit()
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		if db:
			db.close()


def gap(y1, y2):
	return int(y1) - int(y2)


if __name__ == '__main__':
	itr()