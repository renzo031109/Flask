import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="Test1234",
# )
mydb = mysql.connector.connect(user='root', password='Test1234', host='127.0.0.1',port=3306,
auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()
# my_cursor.execute("CREATE DATABASE our_users")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)