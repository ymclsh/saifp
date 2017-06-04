#coding:utf-8
import MySQLdb
import decimal

def itr():
	try:
		db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
		con = db.cursor()
		n = 0
		# find out all the company that have the situations in the 10 years, at one year lost (pft_cat = 1), and one year growing (pft_cat = 6)
		n = con.execute("""SELECT DISTINCT a.symbol FROM earning a, earning b WHERE a.symbol = b.symbol AND a.pft_cat = %s AND b.pft_cat = %s""", (1, 6))
		print n

		for symbol in con.fetchall():
			n = 0
			n = con.execute("""SELECT a.symbol, a.year, a.words_v2, b.pft_cat FROM report a, earning b WHERE a.symbol = %s AND b.symbol = a.symbol AND b.year = a.year""", (symbol, ))

			sum_cat1, n_cat1 = 0, 0
			sum_cat6, n_cat6 = 0, 0
			sum_other, n_other = 0, 0
			avg_words_1, avg_words_6, avg_words_other = decimal.Decimal(0), decimal.Decimal(0), decimal.Decimal(0)
			per = decimal.Decimal(0)

			for year in con.fetchall():
				if year[3] == 1:
					n_cat1 += 1
					sum_cat1 += year[2]
				elif year[3] == 6:
					n_cat6 += 1
					sum_cat6 += year[2]
				else:
					n_other += 1
					sum_other += year[2]
			if n_cat1 > 0 and n_cat6 > 0 and n_other > 0:
				avg_words_1 = sum_cat1 / n_cat1
				avg_words_6 = sum_cat6 / n_cat6
				avg_words_other = sum_other / n_other
				print symbol
				per = avg_words_1 / avg_words_6
				print per
				print avg_words_1
				print avg_words_6
				print avg_words_other


	except MySQLdb.Error, e:
		print e
	finally:
		db.close()



if __name__ == '__main__':
	itr()