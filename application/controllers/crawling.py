from application.models import Models
from application.api import Api
from application.excel import Excel
from flask import request, json, flash

class CrawlingController:
	
	def select_dataCrawling(self):
		instance_Model = Models('SELECT * FROM tbl_tweet_crawling')
		data_crawling = instance_Model.select()
		return data_crawling
	
	def add_dataCrawling(self):
		aksi = request.form['aksi']
		
		instance_Api = Api()
		instance_Excel = Excel()
		
		# Fungsi CARI TWEET(crawling) : Ambil data menggunakan API Twitter ==> Simpan(data) ke Excel & Tampilkan(data) ke layar
		if aksi == 'crawling':
			kata_kunci = request.form['kata_kunci']
			tanggal_awal = request.form['tanggal_awal']
			tanggal_akhir = request.form['tanggal_akhir']
			
			# Ambil data menggunakan API Twitter (Tweepy)
			data_crawling = instance_Api.get_search(kata_kunci +' -filter:retweets', tanggal_awal, tanggal_akhir)
			# Fungsi[1] : Simpan data_crawling ke dalam file Excel
			instance_Excel.save_excel_crawling(data_crawling)
			# Menampilkan data_crawling ke layar
			return json.dumps({ 'data_crawling': data_crawling })
		
		# Fungsi SIMPAN TWEET(crawling) : Ambil data dari excel(yang telah disimpan[1]) ==> Simpan ke Database
		if aksi == 'save_crawling':
			# Fungsi[2] : Membuat tuple dari file excel
			tuples_excel = instance_Excel.make_tuples_crawling()
			
			# Simpan ke Database dengan VALUES berupa tuple dari Fungsi[2]
			instance_Model = Models('REPLACE INTO tbl_tweet_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		
	def import_fileExcelCrawling(self):
		excel_file = request.files['excel_file']

		if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
			instance_Excel = Excel()
			tuples_excel = instance_Excel.make_tuples_crawling(excel_file)
			# Simpan ke Database dengan VALUES berupa tuple
			instance_Model = Models('REPLACE INTO tbl_tweet_crawling(id, text, user, created_at) VALUES (%s, %s, %s, %s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		flash('Format file tidak sesuai! File excel harus ber-ekstensi .xls atau .xlsx', 'error')
		return None
	
	def delete_allDataCrawling(self):
		instance_Model = Models('DELETE FROM tbl_tweet_crawling')
		instance_Model.query_deleteAll()
		return None