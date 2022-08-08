import mysql.connector as connector

def config():
  config = {
    "user": "python",
    "password": "python",
    "host": "localhost",
    "database": "riseshine"
  }
  return config

def DBconnection(config, autocommit):
  connection = connector.connect(**config)
  if autocommit: connection.autocommit=True
  cursor=connection.cursor()
  print('Connection with database established.')
  return [connection,cursor]

def DBend(connection,cursor):
  cursor.close()
  connection.close()
  print('Connection with database closed.')
