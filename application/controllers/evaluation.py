from application.models import Models
from application.vectorizer import Vectorizer
from application.knearestneighbors import KNearestNeighbors
from flask import request, json

class EvaluationController:
	
	def select_dataModel(self):
		instance_Model = Models('SELECT * FROM tbl_model')
		data_model = instance_Model.select()
		return data_model
	
	def count_dataTes(self):
		# HITUNG JUMLAH data testing
		instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_testing WHERE clean_text IS NOT NULL AND sentiment_type IS NOT NULL')
		data_testing = instance_Model.select()
		return data_testing[0]['jumlah']
	
	def check_evaluation(self):
		nilai_k = int(request.form['nilai_k'])
		model_name = request.form['model_name']
		# Select data dari tbl_tweet_testing yang telah diberi label
		instance_Model = Models('SELECT text, clean_text, sentiment_type FROM tbl_tweet_testing WHERE sentiment_type IS NOT NULL')
		tweet_testing_label = instance_Model.select()
		
		tweet_list = []
		teks_list = []
		label_list = []
		for tweet in tweet_testing_label:
			tweet_list.append(tweet['text'])
			teks_list.append(tweet['clean_text'])
			label_list.append(tweet['sentiment_type'])
		
		# Memuat kembali model yang telah dibuat pada proses Pemodelan
		model = json.load(open('application/static/model_data/' +model_name))
		
		# akses ke kelas Vectorizer
		instance_Vectorizer = Vectorizer(teks_list, label_list)
		# membuat vektor berdasarkan model latih
		vector_list = instance_Vectorizer.test_vectorList(model)

		# akses ke kelas KNearestNeighbors
		instance_Klasification = KNearestNeighbors(nilai_k, model)
		data_dict = instance_Klasification.predict_labelList(vector_list)

		confusion_matrix = self.confusion_matrix(label_list, data_dict['label_prediction'])

		# Membandingkan hasil prediksi (hasil) dengan sentimen yang sebenarnya (label_list)
		return json.dumps({ 'tweet_database': tweet_list, 'teks_database': teks_list, 'sentimen_database': label_list, 'data_dict': data_dict, 'confusion_matrix': confusion_matrix })
	
	def select_komposisiModel(self):
		model_name = request.form['model_name']
		instance_Model = Models("SELECT sentiment_count, sentiment_NONHS, sentiment_HS FROM tbl_model WHERE model_name = '"+ model_name +"'")
		komposisi_model = instance_Model.select()
		return komposisi_model
	
	def confusion_matrix(self, label_aktual, label_prediksi):
		true_NONHS = 0
		true_HS = 0
		false_NONHS = 0
		false_HS = 0

		# mencari nilai TP,TN,FP,FN sehingga memperoleh confusion matrix
		for i in range(len(label_aktual)):
			if label_aktual[i] == 'NONHS':	# label aktual bernilai NONHS
				if label_aktual[i] == label_prediksi[i]:	# jika sama-sama NONHS
					true_NONHS += 1
				else:	# jika label aktual bernilai NONHS prediksi bernilai HS
					false_HS += 1
			else:	# label aktual bernilai HS
				if label_aktual[i] == label_prediksi[i]:	# jika sama-sama HS
					true_HS += 1
				else:	# jika label aktual bernilai HS prediksi bernilai NONHS
					false_NONHS += 1
		
		accuration = (true_NONHS+true_HS) / (true_NONHS+true_HS+false_NONHS+false_HS)
		precision = true_NONHS / (true_NONHS+false_NONHS)
		recall = true_NONHS / (true_NONHS+false_HS)

		return {
			'tp': true_NONHS,
			'tn': true_HS,
			'fp': false_NONHS,
			'fn': false_HS,
			'accuration': round(accuration, 2),
			'precision': round(precision, 2),
			'recall': round(recall, 2)
		}
	
	
    