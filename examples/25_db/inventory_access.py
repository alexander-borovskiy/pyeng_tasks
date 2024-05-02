import sqlite3
connection = sqlite3.connect('inventory.db')
cursor = connection.cursor()
#query = """insert into inventory values ('r5', 'Cisco', 'C2911', 'London', '10.5.255.5')"""
#cursor.execute(query)
#connection.commit()
#cursor.execute('select * from inventory')
#while cursor.fetchone():
#	print(cursor.fetchone())

rows = [('sw5', 'Cisco', '3850', 'London', '10.5.254.5'), ('sw6', 'Cisco', '3750', 'London', '10.5.254.6'), ('sw7', 'Cisco', '3850', 'London', '10.5.254.7')]
query = """insert into inventory values (?, ?, ?, ?, ?)"""
#for row in rows:
#	cursor.execute(query, row)
#2
cursor.executemany(query, rows)
connection.commit()
