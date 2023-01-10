from flask import json
from application import mysql

class Models:
	def __init__(self, query):
		self.query = query
		self.conn = mysql.connect()
		self.cursor = self.conn.cursor()
	
	# Fungsi untuk eksekusi perintah TAMPIL data (READ)
	def select(self):
		self.cursor.execute(self.query)
		row_headers = [x[0] for x in self.cursor.description]
		data = self.cursor.fetchall()
		
		self.cursor.close() 
		self.conn.close()
		
		json_data=[]
		for result in data:
			json_data.append(dict(zip(row_headers,result)))
		return json_data
	
	# Fungsi select saru data pertama
	def select_row(self, values):
		self.cursor.execute(self.query, values)
		data = self.cursor.fetchone()
		return data
	
	# Fungsi untuk eksekusi perintah SIMPAN / UBAH / HAPUS data untuk sebuah record (INSERT / UPDATE / DELETE)
	def query_sql(self, values):
		self.cursor.execute(self.query, values)
		self.conn.commit()
		self.cursor.close()
	
	# Fungsi untuk eksekusi perintah TAMBAH / UPDATE data berjumlah > 1 record (INSERT / UPDATE MULTIPLE)
	def query_sql_multiple(self, values):
		self.cursor.executemany(self.query, values)
		self.conn.commit()
		self.cursor.close()
	
	# Fungsi untuk eksekusi perintah HAPUS semua record ( DELETE)
	def query_deleteAll(self):
		self.cursor.execute(self.query)
		self.conn.commit()
		self.cursor.close()