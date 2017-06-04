#coding:utf-8

import MySQLdb
import sys
#import chardet

def to_bytestring(s, enc='utf-8'):
	"""convert the given unicode string to a bytestring, using the standard encoding,
	unless it's already a bytestring"""
	if s:
		if isinstance(s, str):
			return s
		else:
			return s.encode(enc)

def is_chinese(uchar):
	if uchar >= u'/u4e00' and uchar<=u'/u9fa5':
		return True
	else:
		return False
def is_zh(c):
	x = ord(c)
	# Punct & Radicals
	if x >= 0x2e80 and x <= 0x33ff:
		return True
	# Fullwidth Latin Characters
	elif x >= 0xff00 and x <= 0xffef:
		return True
	# CJK Unified Ideographs &
	# CJK Unified Ideographs Extension A
	elif x >= 0x4e00 and x <= 0x9fbb:
		return True
	# CJK Compatibility Ideographs
	elif x >= 0xf900 and x <= 0xfad9:
		return True
	# CJK Unified Ideographs Extension B
	elif x >= 0x20000 and x <= 0x2a6d6:
		return True
	# CJK Compatibility Supplement
	elif x >= 0x2f800 and x <= 0x2fa1d:
		return True
	else:
		return False	

def itr():
	CURRENT_STEP = 2
	MAX_RETURN = 10
	db = MySQLdb.connect(host = "localhost", user = "root", db = "saifp", charset = "utf8")
	cur = db.cursor()
	n = 0
	zh_amt = 0
	avgwords_v2 = 0.0
	sentences_v2 = 0

	cur.execute('SET NAMES UTF8') 

	try:
		while True:
			print "haha"
			try:
				n = 0
				n = cur.execute("""SELECT symbol, year, article, sentences FROM report WHERE process_step <> %s LIMIT %s""", (CURRENT_STEP, MAX_RETURN))
				print n
				if n == 0:
					break
				for row in cur.fetchall():
					print row[0], ":", row[1]
					zh_amt = 0
					avgwords_v2 = 0.0
					sentences_v2 = 0

					for char in row[2]:
						if is_zh(char):
							zh_amt = zh_amt + 1
					if row[3] > 0:
						sentences_v2 = row[3]
						avgwords_v2 = zh_amt / row[3]
					else:
						sentences_v2 = row[2].count(u'。') 
						print "original sentence is zero an now is: ", sentences_v2
					u = """UPDATE report SET avgwords_v2 = %s,  sentences_v2 = %s, words_v2 = %s, process_step = %s WHERE symbol = %s AND year = %s"""
					n = 0
					n = cur.execute(u, (avgwords_v2, sentences_v2, zh_amt, CURRENT_STEP, row[0], row[1]))
					if n == 0:
						db.rollback()
					else:
						db.commit()

			except MySQLdb.Error, e:
				print 'Error %d: %s' % (e.args[0], e.args[1])
	except MySQLdb.Error, e:
		print 'Error %d: %s' % (e.args[0], e.args[1])
	finally:
		if db:
			db.close()


if __name__ == "__main__":
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	itr()