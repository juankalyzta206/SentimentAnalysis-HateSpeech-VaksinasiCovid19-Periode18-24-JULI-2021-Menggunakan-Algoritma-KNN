from application.models import Models
from flask import request
import math
import random

class SplitController:
	
	def count_dataWithLabel(self):
		# SELECT jumlah clean data yang telah memiliki label
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
		data_labeling = instance_Model.select()
		return data_labeling[0]['jumlah']
	
	def add_dataSplit(self):
		rasio = request.form['rasio']
		jumlah_data = float(request.form['jumlah_data'])
		
		if rasio == '1:9':
			jumlah_dataTes = math.floor(jumlah_data * 0.1) # Membagi data sebanyak 10% sebagai data tes(dengan pembulatan ke bawah)
			jumlah_dataLatih = math.ceil(jumlah_data * 0.9) # Membagi data sebanyak 90% sebagai data latih(dengan pembulatan ke atas)
		elif rasio == '2:8':
			jumlah_dataTes = math.floor(jumlah_data * 0.2) # Membagi data sebanyak 20% sebagai data tes(dengan pembulatan ke bawah)
			jumlah_dataLatih = math.ceil(jumlah_data * 0.8) # Membagi data sebanyak 80% sebagai data latih(dengan pembulatan ke atas)
		
		# SPLIT value 0 = data tes	|	value1 = data latih

		# SPLIT SECARA RANDOM / ACAK
		# # Membuat list(data_type) dengan value 0 sebanyak jumlah variabel 'jumlah_dataTes'
		# data_type = [0 for i in range(int(jumlah_dataTes))]
		# # Perulangan untuk mengisi value 1 ke dalam list(data_type) pada index random sebanyak jumlah variabel 'jumlah_dataLatih'
		# for _ in range(int(jumlah_dataLatih)):
		# 	data_type.insert(random.randint(0, len(data_type)), 1)

		# SPLIT SECARA LATIH DULU BARU UJI
		data_type = []
		for i in range(int(jumlah_data)):
			if	i < jumlah_dataLatih:
				data_type.append(1)
			else:
				data_type.append(0)
		
		# SELECT data tweet yang TELAH diberi label untuk diproses
		instance_Model = Models('SELECT * FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
		data_withLabel = instance_Model.select()
		
		data_simpan_tes = []
		data_simpan_latih = []

		# Menyimpan data(yang telah diSELECT) ke tabel yang berbeda berdasarkan value dari variabel 'data_type'
		for index, data in enumerate(data_withLabel):
			if data_type[index] == 0: # Jika value 'data_type' bernilai 0 maka akan di INSERT kedalam tabel TESTING
				data_simpan_tes.append((data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type'])) # Membuat tuple sebagai isian untuk kueri INSERT
			else: # Jika value 'data_type' tidak bernilai 0  INSERT kedalam tabel TRAINING
				data_simpan_latih.append((data['id'], data['text'], data['clean_text'], data['user'], data['created_at'], data['sentiment_type'])) # Membuat tuple sebagai isian untuk kueri INSERT
		
		# Menyimpan data dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
		instance_Model = Models('INSERT IGNORE tbl_tweet_testing(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
		instance_Model.query_sql_multiple(data_simpan_tes)
		# Menyimpan data dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
		instance_Model = Models('INSERT IGNORE tbl_tweet_training(id, text, clean_text, user, created_at, sentiment_type) VALUES (%s, %s, %s, %s, %s, %s)')
		instance_Model.query_sql_multiple(data_simpan_latih)
		return 'true'
	
	def select_dataTraining(self):
		# SELECT data tweet TRAINING
		instance_Model = Models('SELECT * FROM tbl_tweet_training')
		data_training = instance_Model.select()
		return data_training
	
	def select_dataTesting(self):
		# SELECT data tweet TESTING
		instance_Model = Models('SELECT * FROM tbl_tweet_testing')
		data_testing = instance_Model.select()
		return data_testing
	
	def delete_allDataSplit(self):
		instance_Model = Models('DELETE FROM tbl_tweet_training')
		instance_Model.query_deleteAll()
		instance_Model = Models('DELETE FROM tbl_tweet_testing')
		instance_Model.query_deleteAll()
		return None
    