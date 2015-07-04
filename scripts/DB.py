import pyodbc

# uncomment stuff when launching at container
class DBop:
	def __init__(self):
		return
		
		# try:
	 #    	self.connection = pyodbc.connect('TDSVER=8.0 tsql -H XXXXXXXX.database.windows.net -U Username -D DatabaseName -p 1433 -P Password')
  #   	except IOError:
  #   		print('Could not connect to server.')
  #       	sys.exit()

	 #    self.cur = connection.cursor()

	def getNextImage(self):
		return ("01", "img")
		# cur.execute('SELECT data_id, files FROM images_data WHERE status = \'UNPROCESSED\'')

		# cur[0].status = "PROCESSING"
		# return (cur[0].data_id, cur[0].files)

	def save(self, data_id, CNPJ, date, COO, total):
		cur.execute('SELECT * FROM images_data WHERE data_id = \'%s\'' % data_id)

		cur.cnpj = CNPJ
		cur.emission_date = date
		cur.coupon_code = COO
		cur.purchase_value = total
		cur.status = "PROCESSED"