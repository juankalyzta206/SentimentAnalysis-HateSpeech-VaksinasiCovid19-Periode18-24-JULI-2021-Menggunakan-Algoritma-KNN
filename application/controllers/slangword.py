from application.models import Models
from application.excel import Excel
from flask import request, flash

class SlangwordController:
	
	def select_dataSlangword(self):
		instance_Model = Models('SELECT * FROM tbl_slangword')
		data_slangword = instance_Model.select()
		return data_slangword
	
	def add_dataSlangword(self):
		slangword = request.form['slangword'].strip()
		kata_asli = request.form['kata_asli'].strip()
	
		data_tambah = (slangword.lower(), kata_asli.lower())	# Membuat tupple dari form data masukan
	
		instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s,%s)')
		instance_Model.query_sql(data_tambah)
		flash('Berhasil menambahkan data.', 'success')
		return None
	
	def update_dataSlangword(self):
		id = request.form['id']
		slangword = request.form['slangword'].strip()
		kata_asli = request.form['kata_asli'].strip()
	
		data_ubah = (slangword.lower(), kata_asli.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_slangword SET slangword=%s, kata_asli=%s WHERE id_slangword = %s')
		instance_Model.query_sql(data_ubah)
		flash('Berhasil mengubah data.', 'success')
		return None
	
	def delete_dataSlangword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_slangword WHERE id_slangword = %s')
		instance_Model.query_sql(id)
		flash('Berhasil menghapus data.', 'success')
		return None
	
	def import_fileExcelSlangword(self):
		excel_file = request.files['excel_file']

		if(excel_file.filename.lower().endswith(('.xls', '.xlsx'))):
			instance_Excel = Excel()
			tuples_excel = instance_Excel.make_tuples_slangword(excel_file)
			# Simpan ke Database dengan VALUES berupa tuple
			instance_Model = Models('INSERT INTO tbl_slangword(slangword, kata_asli) VALUES (%s, %s)')
			instance_Model.query_sql_multiple(tuples_excel)
			return None
		flash('Format file tidak sesuai! File excel harus ber-ekstensi .xls atau .xlsx', 'error')
		return None
	
	def delete_allDataSlangword(self):
		instance_Model = Models('DELETE FROM tbl_slangword')
		instance_Model.query_deleteAll()
		return None