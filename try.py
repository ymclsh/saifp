
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
	try:
		result = None
		cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='saif')
		cursor = cnx.cursor(buffered = True)

		result = fn(cnx, cursor, **kwargs)

		cnx.commit()

		return result

	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)
	else:
		cursor.close()
		cnx.close()
		return None


def _update_blank_statistics(cnx, cursor):

	curU = cnx.cursor(buffered = True)
	query = ("SELECT symbol, year, avgwords, sentences, words FROM report "
		"WHERE avgwords = 0")

	"""update = ("UPDATE report SET avgwords = %s, sentences = %s, words = %s "
		"WHERE symbol = %s AND year = %s")"""
	updateAvgwords = ("UPDATE report SET avgwords = %s "
			"WHERE symbol = %s AND year = %s")

	cursor.execute(query)
	for (symbol, year, avgwords, sentences, words) in cursor:
		avgwords = 0.0
		if sentences > 0 :
			avgwords = words / sentences
			curU.execute(updateAvgwords, (avgwords, symbol, year))
			print symbol

"""
	for (symbol, year, article, avgwords, sentences, words) in cursor:
		sentences = 0
		words = 0
		avgwords = 0.0
		words = len(article.encode('utf-8'))
		if words > 0 and sentences > 0:
			sentences = article.encode('utf-8').count('。') 
			avgwords = words / sentences
			curU.execute(update, (avgwords, sentences, words, symbol, year))
			print symbol"""

if __name__ == '__main__':
	DBOp(_update_blank_statistics)

