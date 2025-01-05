import sqlite3

connection= sqlite3.connect('student.db')

cursor= connection.cursor()

table_info = """
create table STUDENT(NAME VARCHAR(25), 
CLASS VARCHAR(25), 
SECTION VARCHAR(25), 
MARKS INT);
"""

cursor.execute(table_info)

cursor.execute('''Insert into STUDENT values('Akash','Data Science','A',90)''')
cursor.execute('''Insert into STUDENT values('Aksh','Data Science','B',100)''')
cursor.execute('''Insert into STUDENT values('Ajay','Data Science','A',85)''')
cursor.execute('''Insert into STUDENT values('Arun','Ddevops','A',50)''')
cursor.execute('''Insert into STUDENT values('Akay','web dev','A',35)''')

print("The insreted records are")

data= cursor.execute('''Select * from STUDENT''')

for row in data:
    print(row)

connection.commit()
connection.close()