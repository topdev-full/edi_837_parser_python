import mysql.connector
import uuid
from settings import *

mysql_conn = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  database=MYSQL_DB
)

cursor = mysql_conn.cursor(dictionary=True)

cursor.execute("DELETE FROM matching_837_835")
cursor.execute("DELETE FROM rebound_adjustment")
cursor.execute("DELETE FROM rebound_claim")
cursor.execute("DELETE FROM rebound_diagnosis")
cursor.execute("DELETE FROM rebound_service")

mysql_conn.commit()
mysql_conn.close()