import pyodbc

# still to be tested with container
class DBop:
    def __init__(self):     
        try:
            # TODO: set connection string
            self.connection = pyodbc.connect('DSN=<dsn>;UID=<uid>@<host>;PWD=<pwd>')
        except IOError:
            print('Could not connect to server.')
            sys.exit()

        self.cur = self.connection.cursor()

    def getNextImage(self):
        transaction = 'getReceipt'

        self.cur.execute('BEGIN TRANSACTION %s' % transaction)
        target = self.cur.execute('SELECT data_id, files FROM images_data WHERE status == \'UNPROCESSED\'').fetchone()

        self.cur.execute('UPDATE images_data SET status = %s WHERE data_id == %s' % ('PROCESSING', data_id))

        self.cur.execute('COMMIT TRANSACTION %s' % transaction)

        return (target.data_id, target.files)

    def save(self, data_id, CNPJ, date, COO, total):
        transaction = 'saveReceipt'

        self.cur.execute('BEGIN TRANSACTION %s' % transaction)

        self.cur.execute('UPDATE images_data SET cnpj = %s, emission_date = %s, coupon_code = %s, purchase_value = %s, status = %s WHERE data_id == %s' % (CNPJ, date, COO, total, 'PROCESSED', data_id))

        self.cur.execute('COMMIT TRANSACTION %s' % transaction)

    def check(self):
        check = self.cur.execute('SELECT * FROM images_data WHERE status == \'UNPROCESSED\'')

        if check == None:
            return False
        else:
            return True