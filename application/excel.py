import pandas
from datetime import datetime

class Excel:
	def __init__(self):
		self.file_excelCrawling = 'application/static/excel_data/data_crawling('+ datetime.today().strftime('%d-%m-%Y') +').xlsx'
		self.file_excelPreprocessing = 'application/static/excel_data/data_preprocessing('+ datetime.today().strftime('%d-%m-%Y') +').xlsx'
	
	# Fungsi untuk menyimpan data_crawling ke dalam file excel(.xlsx)
	def save_excel_crawling(self, tweets):
		id = []
		text = []
		username = []
		created_at = []
		
		for tweet in tweets:
			id.append(tweet['id'])
			text.append(str(tweet['full_text']))
			username.append(str(tweet['user']['screen_name']))
			created_at.append(str(tweet['created_at']))
		
		data_frame = pandas.DataFrame({'id': id, 'text': text, 'username': username, 'created_at': created_at})
		data_frame.to_excel(self.file_excelCrawling, index=False)
		
		print('\n\nFile excel(.xlsx) berhasil dibuat.\nLokasi: /:root_project/'+ self.file_excelCrawling +'\n\n')
		return None

	# Fungsi untuk membuat tuple dari data excel slangword yang ada
	def make_tuples_slangword(self, data_frame):
		tweets_container = []
		data_frame = pandas.read_excel(data_frame)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (str(row['slangword']).lower(), str(row['kata_asli']).lower())
			tweets_container.append(tweet_tuple)
		return tweets_container
	
	# Fungsi untuk membuat tuple dari data excel stopword yang ada
	def make_tuples_stopword(self, data_frame):
		tweets_container = []
		data_frame = pandas.read_excel(data_frame)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (str(row['stopword']).lower())
			tweets_container.append(tweet_tuple)
		return tweets_container
	
	# Fungsi untuk membuat tuple dari data excel kata NONHS yang ada
	def make_tuples_positive_word(self, data_frame):
		tweets_container = []
		data_frame = pandas.read_excel(data_frame)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (str(row['positive_word']).lower())
			tweets_container.append(tweet_tuple)
		return tweets_container
	
	# Fungsi untuk membuat tuple dari data excel kata HS yang ada
	def make_tuples_negative_word(self, data_frame):
		tweets_container = []
		data_frame = pandas.read_excel(data_frame)
		
		for index, row in data_frame.iterrows():
			tweet_tuple = (str(row['negative_word']).lower())
			tweets_container.append(tweet_tuple)
		return tweets_container
	
	# Fungsi untuk membuat tuple dari data excel crawling yang ada
	def make_tuples_crawling(self, data_frame=None):
		if data_frame is None:
			data_frame = pandas.read_excel(self.file_excelCrawling)
		else:
			data_frame = pandas.read_excel(data_frame)
		
		# Membuat tuple untuk VALUES insert data
		tweets_container = []
		for index, row in data_frame.iterrows():
			try:
				tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(datetime.strftime(datetime.strptime(row['created_at'],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')))
			except:
				tweet_tuple = (row['id'], str(row['text']), str(row['username']), str(row['created_at']))
			tweets_container.append(tweet_tuple)
		return tweets_container

