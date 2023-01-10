from application.models import Models
from application.excel import Excel
from flask import request, flash

class KamusHSController:
	
	def select_dataHSWord(self):
		instance_Model = Models('SELECT * FROM tbl_lexicon_negative')
		data_negative_word = instance_Model.select()
		return data_negative_word
	
	def add_dataHSWord(self):
		kata_HS = request.form['kata_HS'].strip()

		instance_Model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
		instance_Model.query_sql(kata_HS.lower())
		flash('Berhasil menambahkan data.', 'success')
		return None
	
	def update_dataHSWord(self):
		id = request.form['id']
		kata_HS = request.form['kata_HS'].strip()
	
		data_ubah = (kata_HS.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_lexicon_negative SET negative_word=%s WHERE id_HS = %s')
		instance_Model.query_sql(data_ubah)
		flash('Berhasil mengubah data.', 'success')
		return None
	
	def delete_dataHSWord(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_lexicon_negative WHERE id_HS = %s')
		instance_Model.query_sql(id)
		flash('Berhasil menghapus data.', 'success')
		return None
	
	def import_fileExcelHSWord(self):
		excel_file = request.files['excel_file']
		
		if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
			instance_Excel = Excel()
			tuples_excel = instance_Excel.make_tuples_negative_word(excel_file)
			# Simpan ke Database dengan VALUES berupa tuple
			instance_Model = Models('INSERT INTO tbl_lexicon_negative(negative_word) VALUES (%s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		flash('Format file tidak sesuai! File excel harus ber-ekstensi .xls atau .xlsx', 'error')
		return None
	
	def delete_allDataHSWord(self):
		instance_Model = Models('DELETE FROM tbl_lexicon_negative')
		instance_Model.query_deleteAll()
		return None