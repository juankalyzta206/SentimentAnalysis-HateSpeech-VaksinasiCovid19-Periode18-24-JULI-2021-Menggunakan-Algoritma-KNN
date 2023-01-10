from application.models import Models
from application.excel import Excel
from flask import request, flash

class KamusNONHSController:
	
	def select_dataNONHSWord(self):
		instance_Model = Models('SELECT * FROM tbl_lexicon_positive')
		data_positive_word = instance_Model.select()
		return data_positive_word
	
	def add_dataNONHSWord(self):
		kata_NONHS = request.form['kata_NONHS'].strip()

		instance_Model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
		instance_Model.query_sql(kata_NONHS.lower())
		flash('Berhasil menambahkan data.', 'success')
		return None
	
	def update_dataNONHSWord(self):
		id = request.form['id']
		kata_NONHS = request.form['kata_NONHS'].strip()
	
		data_ubah = (kata_NONHS.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_lexicon_positive SET positive_word=%s WHERE id_NONHS = %s')
		instance_Model.query_sql(data_ubah)
		flash('Berhasil mengubah data.', 'success')
		return None
	
	def delete_dataNONHSWord(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_lexicon_positive WHERE id_NONHS = %s')
		instance_Model.query_sql(id)
		flash('Berhasil menghapus data.', 'success')
		return None
	
	def import_fileExcelNONHSWord(self):
		excel_file = request.files['excel_file']

		if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
			instance_Excel = Excel()
			tuples_excel = instance_Excel.make_tuples_positive_word(excel_file)
			# Simpan ke Database dengan VALUES berupa tuple
			instance_Model = Models('INSERT INTO tbl_lexicon_positive(positive_word) VALUES (%s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		flash('Format file tidak sesuai! File excel harus ber-ekstensi .xls atau .xlsx', 'error')
		return None
	
	def delete_allNONHSWord(self):
		instance_Model = Models('DELETE FROM tbl_lexicon_positive')
		instance_Model.query_deleteAll()
		return None