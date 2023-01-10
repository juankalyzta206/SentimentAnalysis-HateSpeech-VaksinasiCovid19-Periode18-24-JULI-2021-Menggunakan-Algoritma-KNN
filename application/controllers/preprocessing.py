from application.models import Models
from application.excel import Excel
from flask import request, json
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class PreprocessingController:
	
	def select_dataPreprocessing(self):
		# SELECT data preprocessing
		instance_Model = Models('SELECT * FROM tbl_tweet_clean')
		data_preprocessing = instance_Model.select()
		return data_preprocessing
	
	def add_dataPreprocessing(self):
		aksi = request.form['aksi']
		
		instance_Excel = Excel()
		
		# Fungsi PREPROCESSING : Data Tweet dari database ==> PREPROCESSING ==> Tweet Bersih ==> Simpan(data) ke Excel & Tampilkan(data) ke layar
		if aksi == 'preprocessing':
			instance_Model = Models('SELECT * FROM tbl_tweet_crawling')
			data_preprocessing = instance_Model.select()
			
			first_data = []
			last_data = []
			case_folding = []
			remove_non_character = []
			remove_stop_word = []
			change_stemming = []
			change_slang = []

			data_simpan = []

			# Inisialisasi untuk proses 7. Change Slang Word
			instance_Model = Models('SELECT slangword,kata_asli FROM tbl_slangword')
			slangwords = instance_Model.select()
			# Inisialisasi Konfigurasi Library Sastrawi untuk proses Remove Stop Word
			instance_Model = Models('SELECT stopword FROM tbl_stopword')
			stopwords = instance_Model.select()
			# Inisialisasi Konfigurasi Library Sastrawi untuk prosesStemming
			instance_Stemming = StemmerFactory()
			stemmer = instance_Stemming.create_stemmer()

			print('\n-- PROSES '+ str(len(data_preprocessing)) +' DATA --')	# PRINT KE CMD
			for index, data in enumerate(data_preprocessing):
				first_data.append(data['text'])
				
				# Case Folding : Mengubah huruf menjadi huruf kecil
				result_text = data['text'].lower()
				case_folding.append(result_text)
				
				# Remove URL, Mention, Hastag & Number  : Menghilangkan kata yang diawali dengan kata 'http', '@' dan '#'
				result_text = re.sub(r'http\S+|@\S+|#\S+|\d+', '', result_text)
				
				# Remove Selain Huruf : Menghilangkan selain huruf [a-z]
				result_text = re.sub(r'[^a-z ]', '', result_text)
				
				# Remove Whitespace : Menghilangkan spasi/tab/baris yang kosong
				result_text = result_text.strip()
				result_text = re.sub('\s+', ' ', result_text)
				remove_non_character.append(result_text)
				
				# Merubah slang word ke kata aslinya
				for slang in slangwords:
					if slang['slangword'] in result_text:
						result_text = re.sub(r'\b{}\b'.format(slang['slangword']), slang['kata_asli'], result_text)
				change_slang.append(result_text)

				# Menghapus stop word
				for stop in stopwords:
					if stop['stopword'] in result_text:
						result_text = re.sub(r'\b{}\b'.format(stop['stopword']), '', result_text)
				remove_stop_word.append(result_text)
				
				# Stemming : Menghilangkan infleksi/kata berimbuhan kata ke bentuk dasarnya
				result_text = stemmer.stem(result_text)
				change_stemming.append(result_text)

				last_data.append(result_text)
 
				if result_text != '':
					# SIMPAN DATA
					try:
						data_simpan.append((data['id'], data['text'], result_text, data['user'], data['created_at'])) # Membuat tuple sebagai isian untuk kueri INSERT
					except:
						print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
				else:
					print('\nGagal Menyimpan Data (ID: '+ str(data['id']) +')\n')
				print(index+1)	# PRINT KE CMD
			
			# Menyimpan data hasil preprocessing dengan kueri INSERT IGNORE, dengan memperbarui record yang duplikat berdasarkan PK
			instance_Model = Models('REPLACE INTO tbl_tweet_clean(id, text, clean_text, user, created_at) VALUES (%s, %s, %s, %s, %s)')
			instance_Model.query_sql_multiple(data_simpan)
			
			print('\n-- SELESAI --\n')	# PRINT KE CMD
			
			# Menampilkan data ke layar
			return json.dumps({'first_data': first_data, 'case_folding': case_folding, 'remove_non_character': remove_non_character, 'change_slang': change_slang, 'remove_stop_word': remove_stop_word, 'change_stemming': change_stemming, 'last_data': last_data})
	
	def count_dataCrawling(self):
		# SELECT jumlah data crawling
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
		data_crawling = instance_Model.select()
		return data_crawling[0]['jumlah']
	
	def delete_allDataPreprocessing(self):
		instance_Model = Models('DELETE FROM tbl_tweet_clean WHERE sentiment_type IS NULL')
		instance_Model.query_deleteAll()
		return None