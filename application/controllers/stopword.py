from application.models import Models
from application.excel import Excel
from flask import request, flash

class StopwordController:
	
	def select_dataStopword(self):
		instance_Model = Models('SELECT * FROM tbl_stopword')
		data_stopword = instance_Model.select()
		return data_stopword
	
	def add_dataStopword(self):
		stopword = request.form['stopword'].strip()
	
		instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
		instance_Model.query_sql(stopword.lower())
		flash('Berhasil menambahkan data.', 'success')
		return None
	
	def update_dataStopword(self):
		id = request.form['id']
		stopword = request.form['stopword'].strip()
	
		data_ubah = (stopword.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_stopword SET stopword=%s WHERE id_stopword = %s')
		instance_Model.query_sql(data_ubah)
		flash('Berhasil mengubah data.', 'success')
		return None
	
	def delete_dataStopword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_stopword WHERE id_stopword = %s')
		instance_Model.query_sql(id)
		flash('Berhasil menghapus data.', 'success')
		return None
		
	def import_fileExcelStopword(self):
		excel_file = request.files['excel_file']

		if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
			instance_Excel = Excel()
			tuples_excel = instance_Excel.make_tuples_stopword(excel_file)
			# Simpan ke Database dengan VALUES berupa tuple
			instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		flash('Format file tidak sesuai! File excel harus ber-ekstensi .xls atau .xlsx', 'error')
		return None
	
	def delete_allDataStopWord(self):
		instance_Model = Models('DELETE FROM tbl_stopword')
		instance_Model.query_deleteAll()
		return None
	