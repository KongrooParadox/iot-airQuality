from influxdb import InfluxDBClient

DELAY = 10
HOST = 'localhost'
DBNAME = 'iot'
USER = 'pi'
PWD = 'raspberry'

def main():
	try:
		client = InfluxDBClient(HOST, 8086, USER, PWD, DBNAME)

		client.create_database(DBNAME)

		print("Create retention policy")
		client.create_retention_policy('one_day_only', '1d', 1, default=True)

if __name__ == '__main__':
	main()
