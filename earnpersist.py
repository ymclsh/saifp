#coding:utf-8
import MySQLdb
import decimal

def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		con = db.cursor()
		n = 0
		n = con.execute("""SELECT DISTINCT symbol FROM earning""")
		symbols = con.fetchall()

		for symbol in symbols:
			n = 0
			n = con.execute("""SELECT * FROM earning where symbol = %s AND rev != %s AND pft != %s""", (symbol, 0, 0))

			earnings = con.fetchall()
			earnings = sorted(earnings, key = lambda x:x[1], reverse = True)

			following_rev, following_pft = decimal.Decimal(0), decimal.Decimal(0)
			current_rev, current_pft = decimal.Decimal(0), decimal.Decimal(0)
			"""
					tag:
					0: last year, nothing indicates
					1: current +, following -  f/c < 0;			first year lost
					2: current +, following +, 0 < f/c < 1 ; 	reduce
					3: current -, following -, 		f/c > 1;    loss expand
					4: current -, following -, 0 < f/c < 1; 	loss reduce
					5: current -, following +, 	f/c < 0;		first year profitable
					6: current +, following +,  f/c > 1;		growing
			"""

			for current in earnings:

				rev_cat, pft_cat = 0, 0
				rev_rate, pft_rate = 0.0, 0.0

				current_rev = current[2]
				current_pft = current[3]
				
				if current[1] != '2015':

					if current_rev != 0:

						rev_rate = following_rev / current_rev

						if current_rev > 0:

							if rev_rate < 0:
								rev_cat = 1
							elif rev_rate < 1 and rev_rate > 0 :
								rev_cat = 2
							elif rev_rate > 1:
								rev_cat = 6

						elif current_rev < 0:

							if rev_rate < 0:
								rev_cat = 5
							elif rev_rate <1 and rev_rate > 0:
								rev_cat = 4
							elif rev_rate > 1:
								rev_cat = 3

					if current_pft != 0:

						pft_rate = following_pft / current_pft

						if current_pft > 0:

							if pft_rate < 0:
								pft_cat = 1
							elif pft_rate < 1 and pft_rate > 0:
								pft_cat = 2
							elif pft_rate > 1:
								pft_cat = 6

						elif current_pft < 0:

							if pft_rate < 0:
								pft_cat = 5
							elif pft_rate < 1 and pft_rate > 0:
								pft_cat = 4
							elif pft_rate > 1:
								pft_cat = 3

				#update database

				u = """UPDATE earning SET rev_cat = %s, pft_cat = %s, rev_rate = %s, pft_rate = %s WHERE year = %s AND symbol = %s"""
				n = 0
				n = con.execute(u, (rev_cat, pft_cat, rev_rate, pft_rate, current[1], current[0]))
				print n
				db.commit()

				following_rev, following_pft = current_rev, current_pft				

	except MySQLdb.Error, e:
		pass
	finally:
		db.close()

if __name__ == '__main__':
	itr()