from influxdb import InfluxDBClient

DELAY = 10
HOST = 'localhost'
DBNAME = 'iot'
USER = 'pi'
PWD = 'raspberry'

def main():
	try:
		client = InfluxDBClient(HOST, 8086, USER, PWD, DBNAME)

		print("Drop database: {}".format(DBNAME))
		client.drop_database(DBNAME)

if __name__ == '__main__':
	main()
