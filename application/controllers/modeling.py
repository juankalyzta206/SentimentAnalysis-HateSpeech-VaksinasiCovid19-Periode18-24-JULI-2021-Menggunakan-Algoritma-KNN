from application.models import Models
from application.vectorizer import Vectorizer
from flask import request, json, flash
from datetime import datetime
import os

class ModelingController:
	
	def count_dataTraining(self):
		# SELECT data training
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_training = instance_Model.select()
		return data_training[0]['jumlah']
	
	def select_dataModel(self):
		instance_Model = Models('SELECT * FROM tbl_model')
		data_model = instance_Model.select()
		return data_model
	
	def create_dataModeling(self):
		sample_NONHS = request.form['sample_NONHS']
		sample_HS = request.form['sample_HS']
		jumlah_sample = int(sample_NONHS) + int(sample_HS)

		# if sample_NONHS == sample_HS == sample_netral:
		if sample_NONHS == sample_HS:
			list_data = [] # wadah untuk menyimpan data yang diperoleh dari database

			# Select data NONHS dari tbl_tweet_training sebanyak n record (berdasarkan variabel sample)
			instance_Model = Models("SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type = 'NONHS' ORDER BY RAND() LIMIT "+ sample_NONHS)
			list_data.append(instance_Model.select())
			# Select data HS dari tbl_tweet_training sebanyak n record (berdasarkan variabel sample)
			instance_Model = Models("SELECT clean_text, sentiment_type FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type = 'HS' ORDER BY RAND() LIMIT "+ sample_HS)
			list_data.append(instance_Model.select())

			teks_list = [] # wadah untuk tweet (clean_text) yang akan dijadikan sebagai model latih
			label_list = [] # wadah untuk sentimen (sentiment_type) yang akan dijadikan sebagai model latih

			# set data untuk teks_list dan label_list menggunakan data yang telah diambil dari database
			# for index_luar in range(3):
			for index_luar in range(2):
				for index_dalam in range(len(list_data[index_luar])):
					clean_text = list_data[index_luar][index_dalam]['clean_text']
					sentiment_type = list_data[index_luar][index_dalam]['sentiment_type']

					teks_list.append(clean_text)
					label_list.append(sentiment_type)
			
			# akses ke kelas Vectorizer
			instance_Vectorizer = Vectorizer(teks_list, label_list)
			# membuat vektor angka
			data_dict = instance_Vectorizer.create_vectorList()

			model_name = 'sentiment_model('+ datetime.today().strftime('%d-%m-%Y %H%M%S') +').json'
			# model_name = 'sentiment_model('+ datetime.today().strftime('%d-%m-%Y') +').json'

			# Menyimpan model kedalam bentuk .json agar dapat digunakan kembali (untuk proses Evaluasi & Prediksi)
			with open('application/static/model_data/'+ model_name, 'w') as outfile:
				json.dump(data_dict, outfile, indent=4)

			# Membuat tuple untuk simpan data
			data_simpan = (model_name, jumlah_sample, sample_NONHS, sample_HS)

			# Insert model ke dalam database
			instance_Model = Models('REPLACE INTO tbl_model(model_name, sentiment_count, sentiment_NONHS, sentiment_HS) VALUES (%s, %s, %s, %s)')
			# Menjadikan tuple sebagai argumen untuk method query_sql
			instance_Model.query_sql(data_simpan)

			return { 'model_name': model_name, 'sentiment_count': jumlah_sample, 'sentiment_NONHS': sample_NONHS, 'sentiment_HS': sample_HS, 'data_dict': data_dict }
		return  { 'error': 'Gagal Membuat Model Latih' }
	
	def delete_dataModelling(self):
		id = request.form['id']
		
		instance_Model = Models('DELETE FROM tbl_model WHERE model_name = %s')
		instance_Model.query_sql(id)

		if os.path.exists('application/static/model_data/'+ id):
			os.remove('application/static/model_data/'+ id)
			flash('Berhasil menghapus data. File (.json) model latih berhasil dihapus!', 'success')
		else:
			flash('File (.json) model latih gagal dihapus!', 'error')
			print("\nFile tidak ditemukan!\n")
	
	def count_sampleSentiment(self):
		# SELECT jumlah data training berdasarkan jenis sentimen
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL GROUP BY sentiment_type')
		data_max_sentiment = instance_Model.select()

		min = 999999	# asumsi jumlah minimal sentimen tidak lebih dari 999999
		# mencari jumlah minimal sentimen
		for data in data_max_sentiment:
			if data['jumlah'] < min:
				min = data['jumlah']
		
		if min == 999999:
			min = 0
		
		# nilai variable 'min' digunakan sebagai batas atas sample sentimen & nilai 'min*2' digunakan untuk mengetahui jumlah kuota sample
		return min, min*2
    