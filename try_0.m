conn = database('saifp', 'root', '', 'com.mysql.jdbc.Driver', 'jdbc:mysql://localhost:3306/saifp')

cur = exec(conn, 'select a.symbol, a.year, a.words_v2, b.pft_rate from saifp.report as a, saifp.earning as b where a.symbol = b.symbol and a.year = b.year and b.pft_rate != 0')


