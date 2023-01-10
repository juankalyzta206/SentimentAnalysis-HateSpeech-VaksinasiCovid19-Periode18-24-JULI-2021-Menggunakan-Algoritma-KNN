from flask import render_template, request, redirect, url_for
from application import app
from application.controllers.auth import AuthController
from application.controllers.dashboard import DashboardController
from application.controllers.slangword import SlangwordController
from application.controllers.stopword import StopwordController
from application.controllers.kamuspositif import KamusNONHSController
from application.controllers.kamusnegatif import KamusHSController
from application.controllers.crawling import CrawlingController
from application.controllers.preprocessing import PreprocessingController
from application.controllers.labeling import LabelingController
from application.controllers.split import SplitController
from application.controllers.modeling import ModelingController
from application.controllers.evaluation import EvaluationController

controller_auth = AuthController()	# Menetapkan Instance dari Class AuthController ================

# Tampil Halaman(VIEW) masuk aplikasi
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		controller_auth.logout()	# Memanggil fungsi 'logout()' menggunakan Instance 'controller_auth'
		return render_template('login.html', error=False)	# Akses ke halaman/view login
	
	if request.method == 'POST':
		response = controller_auth.login()	# Memanggil fungsi 'login()' menggunakan Instance 'controller_auth'
		if response:
			return redirect(url_for('dashboard'))	# Memanggil fungsi dashboard() dengan method GET
		return render_template('login.html', error=True)	# Akses ke halaman/view login dengan error

# Fungsi keluar (logout) aplikasi
@app.route('/logout', methods=['GET'])
def logout():
	controller_auth.logout()	# Memanggil fungsi 'logout()' menggunakan Instance 'controller_auth'
	return redirect(url_for('login'))	# Memanggil fungsi login() dengan method GET

# Fungsi daftar akun
@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'GET':
		controller_auth.logout()	# Memanggil fungsi 'logout()' menggunakan Instance 'controller_auth'
		return render_template('register.html')	# Akses ke halaman/view register
	
	if request.method == 'POST':
		response = controller_auth.register()	# Memanggil fungsi 'register()' menggunakan Instance 'controller_auth'
		if response:
			return redirect(url_for('register'))	# Memanggil fungsi register() dengan method GET
		return render_template('register.html')	# Akses ke halaman/view register dengan error

controller_dashboard = DashboardController()	# Menetapkan Instance dari Class DashboardController ================

# Tampil Halaman(VIEW) Beranda
@app.route('/dashboard')
def dashboard():
	data = controller_dashboard.getData()	# Memanggil fungsi 'getData()' menggunakan Instance 'controller_slangword'
	return render_template('dashboard.html', data=data)

controller_slangword = SlangwordController()	# Menetapkan Instance dari Class SlangwordController ================

# Tampil Halaman(VIEW) & Simpan Data Slangword
@app.route('/slangword', methods=['GET','POST'])
def slangword():
	if request.method == 'GET':
		return render_template('slangword.html')	# Akses ke halaman/view slangword
	
	if request.method == 'POST':
		controller_slangword.add_dataSlangword()	# Memanggil fungsi 'add_dataSlangword()' menggunakan Instance 'controller_slangword'
	
	return redirect(url_for('slangword'))	# Memanggil fungsi slangword() dengan method GET

# Tampil Data ke dalam tabel Slangword
@app.route('/list_slangword', methods=['GET'])
def list_slangword():
	data_slangword = controller_slangword.select_dataSlangword()	# Memanggil fungsi 'select_dataSlangword()' menggunakan Instance 'controller_slangword'
	return { 'data': data_slangword }

# Ubah Data Slangword
@app.route('/slangword/ubah', methods=['POST'])
def ubah_dataSlangword():
	controller_slangword.update_dataSlangword()	# Memanggil fungsi 'update_dataSlangword()' menggunakan Instance 'controller_slangword'
	return redirect(url_for('slangword'))

# Hapus Data Slangword
@app.route('/slangword/hapus', methods=['POST'])
def hapus_dataSlangword():
	controller_slangword.delete_dataSlangword()	# Memanggil fungsi 'delete_dataSlangword()' menggunakan Instance 'controller_slangword'
	return redirect(url_for('slangword'))

# Import file excel proses Slangword data
@app.route('/importSlangword', methods=['POST'])
def importSlangword():
	controller_slangword.import_fileExcelSlangword()
	return redirect(url_for('slangword'))	# Memanggil fungsi 'slangword()' dengan method GET

# Hapus Data kata Slangword
@app.route('/slangword/hapus-all', methods=['POST'])
def hapus_allDataSlangword():
	controller_slangword.delete_allDataSlangword()	# Memanggil fungsi 'delete_allDataSlangword()' menggunakan Instance 'controller_slangword'
	return redirect(url_for('slangword'))

controller_stopword = StopwordController()	# Menetapkan Instance dari Class StopwordController ================

# Tampil Halaman(VIEW) & Simpan Data Stopword
@app.route('/stopword', methods=['GET','POST'])
def stopword():
	if request.method == 'GET':
		return render_template('stopword.html')	# Akses ke halaman/view stopword
	
	if request.method == 'POST':
		controller_stopword.add_dataStopword()	# Memanggil fungsi 'add_dataStopword()' menggunakan Instance 'controller_stopword'
	
	return redirect(url_for('stopword'))	# Memanggil fungsi stopword() dengan method GET

# Tampil Data ke dalam tabel Stopword
@app.route('/list_stopword', methods=['GET'])
def list_stopword():
	data_stopword = controller_stopword.select_dataStopword()	# Memanggil fungsi 'select_dataStopword()' menggunakan Instance 'controller_stopword'
	return { 'data': data_stopword }

# Ubah Data Stopword 
@app.route('/stopword/ubah', methods=['POST'])
def ubah_dataStopword():
	controller_stopword.update_dataStopword()	# Memanggil fungsi 'update_dataStopword()' menggunakan Instance 'controller_stopword'
	return redirect(url_for('stopword'))

# Hapus Data Stopword
@app.route('/stopword/hapus', methods=['POST'])
def hapus_dataStopword():
	controller_stopword.delete_dataStopword()	# Memanggil fungsi 'delete_dataStopword()' menggunakan Instance 'controller_stopword'
	return redirect(url_for('stopword'))

# Import file excel proses Stopword data
@app.route('/importStopword', methods=['POST'])
def importStopword():
	controller_stopword.import_fileExcelStopword()
	return redirect(url_for('stopword'))	# Memanggil fungsi 'stopword()' dengan method GET

# Hapus Data kata stopword
@app.route('/stopword/hapus-all', methods=['POST'])
def hapus_allDataStopWord():
	controller_stopword.delete_allDataStopWord()	# Memanggil fungsi 'delete_allDataStopWord()' menggunakan Instance 'controller_stopword'
	return redirect(url_for('stopword'))

controller_kamusNONHS = KamusNONHSController()	# Menetapkan Instance dari Class KamusNONHSController ================

# Tampil Halaman(VIEW) & Simpan Data kata NONHS
@app.route('/NONHS-word', methods=['GET','POST'])
def positive_word():
	if request.method == 'GET':
		return render_template('positive_word.html')	# Akses ke halaman/view positive_word
	
	if request.method == 'POST':
		controller_kamusNONHS.add_dataNONHSWord()	# Memanggil fungsi 'add_dataNONHSWord()' menggunakan Instance 'controller_kamusNONHS'
	
	return redirect(url_for('positive_word'))	# Memanggil fungsi positive_word() dengan method GET

# Tampil Data ke dalam tabel kata NONHS
@app.route('/list_positive_word', methods=['GET'])
def list_positive_word():
	data_positive_word = controller_kamusNONHS.select_dataNONHSWord()	# Memanggil fungsi 'select_dataNONHSWord()' menggunakan Instance 'controller_kamusNONHS'
	return { 'data': data_positive_word }

# Ubah Data kata NONHS
@app.route('/NONHS-word/ubah', methods=['POST'])
def ubah_positive_word():
	controller_kamusNONHS.update_dataNONHSWord()	# Memanggil fungsi 'update_dataNONHSWord()' menggunakan Instance 'controller_kamusNONHS'
	return redirect(url_for('positive_word'))

# Hapus Data kata NONHS
@app.route('/NONHS-word/hapus', methods=['POST'])
def hapus_positive_word():
	controller_kamusNONHS.delete_dataNONHSWord()	# Memanggil fungsi 'delete_dataNONHSWord()' menggunakan Instance 'controller_kamusNONHS'
	return redirect(url_for('positive_word'))

# Import file excel proses data kata NONHS
@app.route('/importpositive_word', methods=['POST'])
def importpositive_word():
	controller_kamusNONHS.import_fileExcelNONHSWord()
	return redirect(url_for('positive_word'))	# Memanggil fungsi 'positive_word()' dengan method GET

# Hapus Data kata HS
@app.route('/NONHS-word/hapus-all', methods=['POST'])
def hapus_allNONHSWord():
	controller_kamusNONHS.delete_allNONHSWord()	# Memanggil fungsi 'delete_allDataNONHSWord()' menggunakan Instance 'controller_kamusNONHS'
	return redirect(url_for('positive_word'))

controller_kamusHS = KamusHSController()	# Menetapkan Instance dari Class KamusHSController ================

# Tampil Halaman(VIEW) & Simpan Data kata HS
@app.route('/HS-word', methods=['GET','POST'])
def negative_word():
	if request.method == 'GET':
		return render_template('negative_word.html')	# Akses ke halaman/view negative_word
	
	if request.method == 'POST':
		controller_kamusHS.add_dataHSWord()	# Memanggil fungsi 'add_dataHSWord()' menggunakan Instance 'controller_kamusHS'
	
	return redirect(url_for('negative_word'))	# Memanggil fungsi positive_word() dengan method GET

# Tampil Data ke dalam tabel kata HS
@app.route('/list_negative_word', methods=['GET'])
def list_negative_word():
	data_negative_word = controller_kamusHS.select_dataHSWord()	# Memanggil fungsi 'select_dataHSWord()' menggunakan Instance 'controller_kamusHS'
	return { 'data': data_negative_word }

# Ubah Data kata HS
@app.route('/HS-word/ubah', methods=['POST'])
def ubah_negative_word():
	controller_kamusHS.update_dataHSWord()	# Memanggil fungsi 'update_dataHSWord()' menggunakan Instance 'controller_kamusHS'
	return redirect(url_for('negative_word'))

# Hapus Data kata HS
@app.route('/HS-word/hapus', methods=['POST'])
def hapus_negative_word():
	controller_kamusHS.delete_dataHSWord()	# Memanggil fungsi 'delete_dataHSWord()' menggunakan Instance 'controller_kamusHS'
	return redirect(url_for('negative_word'))

# Import file excel proses data kata HS
@app.route('/importnegative_word', methods=['POST'])
def importnegative_word():
	controller_kamusHS.import_fileExcelHSWord()
	return redirect(url_for('negative_word'))	# Memanggil fungsi 'negative_word()' dengan method GET

# Hapus Data kata HS
@app.route('/HS-word/hapus-all', methods=['POST'])
def hapus_allDataHSWord():
	controller_kamusHS.delete_allDataHSWord()	# Memanggil fungsi 'delete_allDataHSWord()' menggunakan Instance 'controller_kamusHS'
	return redirect(url_for('negative_word'))

controller_crawling = CrawlingController()	# Menetapkan Instance dari Class CrawlingController ================

# Tampil Halaman(VIEW) & Simpan Data Crawling
@app.route('/crawling', methods=['GET','POST'])
def crawling():
	if request.method == 'GET':
		return render_template('crawling.html')
	
	if request.method == 'POST':
		response = controller_crawling.add_dataCrawling()	# Memanggil fungsi 'add_dataCrawling()' menggunakan Instance 'controller_crawling'
		if response != None:
			return response
		
		return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET

# Tampil Data ke dalam tabel Crawling
@app.route('/list_data_crawling', methods=['GET'])
def list_data_crawling():
	data_crawling = controller_crawling.select_dataCrawling()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller_crawling'
	return { 'data': data_crawling }

# Import file excel proses Crawling data
@app.route('/importCrawling', methods=['POST'])
def importCrawling():
	controller_crawling.import_fileExcelCrawling()
	return redirect(url_for('crawling'))	# Memanggil fungsi 'crawling()' dengan method GET

# Hapus Data Crawling
@app.route('/crawling/hapus-all', methods=['POST'])
def hapus_allDataCrawling():
	controller_crawling.delete_allDataCrawling()	# Memanggil fungsi 'delete_allDataCrawling()' menggunakan Instance 'controller_crawling'
	return redirect(url_for('crawling'))

controller_preprocessing = PreprocessingController()	# Menetapkan Instance dari Class PreprocessingController ================

# Tampil Halaman(VIEW) & Simpan Data Preprocessing
@app.route('/preprocessing', methods=['GET','POST'])
def preprocessing():
	if request.method == 'GET':
		count_data_crawling = controller_preprocessing.count_dataCrawling()	# Memanggil fungsi 'count_dataCrawling()' menggunakan Instance 'controller_preprocessing'
		return render_template('preprocessing.html', count_data_crawling=count_data_crawling)
	
	if request.method == 'POST':
		response = controller_preprocessing.add_dataPreprocessing()	# Memanggil fungsi 'add_dataPreprocessing()' menggunakan Instance 'controller_preprocessing'
		return response

# Tampil Data ke dalam tabel preprocessing
@app.route('/list_data_preprocessing', methods=['GET'])
def list_data_preprocessing():
	data_preprocessing = controller_preprocessing.select_dataPreprocessing()	# Memanggil fungsi 'select_dataPreprocessing()' menggunakan Instance 'controller_preprocessing'
	return { 'data': data_preprocessing }

# Hapus Data Preprocessing
@app.route('/preprocessing/hapus-all', methods=['POST'])
def hapus_allDataPreprocessing():
	controller_preprocessing.delete_allDataPreprocessing()	# Memanggil fungsi 'delete_allDataPreprocessing()' menggunakan Instance 'controller_preprocessing'
	return redirect(url_for('preprocessing'))

controller_labeling = LabelingController()	# Menetapkan Instance dari Class LabelingController ================

# Tampil Halaman(VIEW) & Simpan Labeling Data
@app.route('/labeling', methods=['GET','POST'])
def labeling():
	if request.method == 'GET':
		count_data_no_label = controller_labeling.count_dataNoLabel()	# Memanggil fungsi 'count_dataNoLabel()' menggunakan Instance 'controller_labeling'
		return render_template('labeling.html', count_data_no_label=count_data_no_label)
	
	if request.method == 'POST':
		response = controller_labeling.add_dataLabeling()	# Memanggil fungsi 'add_dataLabeling()' menggunakan Instance 'controller_labeling'
		return response

# Labeling dengan Kamus sentimen
@app.route('/labeling_kamus', methods=['POST'])
def labeling_kamus():
	response = controller_labeling.add_dataLabelingKamus()	# Memanggil fungsi 'add_dataLabelingKamus()' menggunakan Instance 'controller_labeling'
	return response

# Tampil Data BERLABEL ke dalam tabel labeling
@app.route('/list_data_with_label', methods=['GET'])
def list_data_with_label():
	data_with_label = controller_labeling.select_dataWithLabel()	# Memanggil fungsi 'select_dataWithLabel()' menggunakan Instance 'controller_labeling'
	return { 'data': data_with_label }

# Tampil Data NO-LABEL ke dalam tabel labeling
@app.route('/list_data_no_label', methods=['GET'])
def list_data_no_label():
	data_no_label = controller_labeling.select_dataNoLabel()	# Memanggil fungsi 'select_dataNoLabel()' menggunakan Instance 'controller_labeling'
	return { 'data': data_no_label }

# Hapus Data labeling
@app.route('/labeling/hapus-all', methods=['POST'])
def hapus_allDataLabeling():
	controller_labeling.delete_allDataLabeling()	# Memanggil fungsi 'delete_allDataLabeling()' menggunakan Instance 'controller_labeling'
	return redirect(url_for('labeling'))

controller_split = SplitController()	# Menetapkan Instance dari Class SplitController ================

# Tampil Halaman(VIEW) & Simpan Split Data
@app.route('/split', methods=['GET','POST'])
def split():
	if request.method == 'GET':
		count_data_with_label = controller_split.count_dataWithLabel()	# Memanggil fungsi 'count_dataWithLabel()' menggunakan Instance 'controller_split'
		return render_template('split.html', count_data_with_label=count_data_with_label)
	
	if request.method == 'POST':
		response = controller_split.add_dataSplit()	# Memanggil fungsi 'add_dataSplit()' menggunakan Instance 'controller_split'
		return response

# Tampil Data TRAINING ke dalam tabel split
@app.route('/list_data_training', methods=['GET'])
def list_data_training():
	data_training = controller_split.select_dataTraining()	# Memanggil fungsi 'select_dataTraining()' menggunakan Instance 'controller_split'
	return { 'data': data_training }

# Tampil Data TESTING ke dalam tabel split
@app.route('/list_data_testing', methods=['GET'])
def list_data_testing():
	data_testing = controller_split.select_dataTesting()	# Memanggil fungsi 'select_dataTesting()' menggunakan Instance 'controller_split'
	return { 'data': data_testing }

# Hapus Data labeling
@app.route('/split/hapus-all', methods=['POST'])
def hapus_allDataSplit():
	controller_split.delete_allDataSplit()	# Memanggil fungsi 'delete_allDataSplit()' menggunakan Instance 'controller_split'
	return redirect(url_for('split'))

controller_modeling = ModelingController()	# Menetapkan Instance dari Class ModelingController ================

# Modelling Data
@app.route('/modeling', methods=['GET','POST'])
def modeling():
	if request.method == 'GET':
		data_model = controller_modeling.select_dataModel()	# Memanggil fungsi 'select_dataModel()' menggunakan Instance 'controller_modeling'
		count_data_training = controller_modeling.count_dataTraining()	# Memanggil fungsi 'count_dataTraining()' menggunakan Instance 'controller_modeling'
		max_sample_sentiment, total_sample_sentiment = controller_modeling.count_sampleSentiment()	# Memanggil fungsi 'count_sampleSentiment()' menggunakan Instance 'controller_modeling'
		return render_template('modeling.html', data_model=data_model, count_data_training=count_data_training, max_sample_sentiment=max_sample_sentiment, total_sample_sentiment=total_sample_sentiment)
	
	if request.method == 'POST':
		response = controller_modeling.create_dataModeling()	# Memanggil fungsi 'create_dataModeling()' menggunakan Instance 'controller_modeling'
		return response

# Hapus Data Model
@app.route('/modeling/hapus', methods=['POST'])
def hapus_dataModelling():
	controller_modeling.delete_dataModelling()	# Memanggil fungsi 'delete_dataModelling()' menggunakan Instance 'controller_modeling'
	return redirect(url_for('modeling'))

controller_evaluation = EvaluationController()	# Menetapkan Instance dari Class EvaluationController ================

# Pengujian Data
@app.route('/evaluation', methods=['GET','POST'])
def evaluation():
	if request.method == 'GET':
		count_data_testing = controller_evaluation.count_dataTes()	# Memanggil fungsi 'count_dataTes()' menggunakan Instance 'controller_evaluation'
		data_model = controller_evaluation.select_dataModel()	# Memanggil fungsi 'select_dataCrawling()' menggunakan Instance 'controller_evaluation'
		return render_template('evaluation.html', data_model=data_model, count_data_testing=count_data_testing)
	
	if request.method == 'POST':
		response = controller_evaluation.check_evaluation()	# Memanggil fungsi 'check_evaluation()' menggunakan Instance 'controller_evaluation'
		return response

# Tampil KOMPOSISI model
@app.route('/komposisi_model', methods=['POST'])
def komposisi_model():
	komposisi_model = controller_evaluation.select_komposisiModel()	# Memanggil fungsi 'select_komposisiModel()' menggunakan Instance 'controller_evaluation'
	return { 'data': komposisi_model }
