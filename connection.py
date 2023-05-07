import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",password="Ishu@80742683")
print(mydb.connection_id)
cur=mydb.cursor()
cur.execute('create database IR')

