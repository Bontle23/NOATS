import mysql.connector
import datetime


mydb = mysql.connector.connect(user = "root", database="eee4022s", passwd = "me", host="localhost")
#cnx = mysql.connector.connect(user='root', database='eee4022s')
#cnx = mysql.connector.connect(user='root', password='me', host='localhost', database='eee4022s')
mycursor = mydb.cursor()

sql = "INSERT INTO loggedData (time_stamp, temp_1) VALUES (%s, %s)"

val = (datetime.datetime.now(), 24)

mycursor.execute(sql, val)

mydb.commit()
