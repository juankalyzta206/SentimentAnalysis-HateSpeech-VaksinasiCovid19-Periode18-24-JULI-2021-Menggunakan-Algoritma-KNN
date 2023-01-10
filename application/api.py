from application import api
import datetime

class Api:
	
	# Fungsi untuk mengambil data search dari Twitter
	def get_search(self, kata_kunci, tanggal_awal, tanggal_akhir):
		startDate =	datetime.datetime.strptime(tanggal_awal, '%Y-%m-%d')
		endDate = datetime.datetime.strptime(tanggal_akhir, '%Y-%m-%d')
		endDate	=  endDate.replace(hour=23, minute=59, second=59)
		
		tweets = []
		
		# Loop untuk mengambil data search hari ini
		search = api.search(kata_kunci, lang='id', result_type='recent', tweet_mode='extended')
		for tweet in search:
			if tweet.created_at < endDate and tweet.created_at > startDate:
				tweets.append(tweet._json)	# Menambahkan data ke dalam Array
		
		# Loop untuk mengambil data search hari kemarin sampai dengan startDate
		while (search[-1].created_at > startDate):
			print('Tweet @', search[-1].created_at, ' - Berjalan...')
			search = api.search(kata_kunci, lang='id', result_type='recent', tweet_mode='extended', max_id=search[-1].id)
			for tweet in search:
				if tweet.created_at < endDate and tweet.created_at > startDate and not tweet._json in tweets:
					tweets.append(tweet._json)	# Menambahkan data ke dalam Array
		
		return tweets