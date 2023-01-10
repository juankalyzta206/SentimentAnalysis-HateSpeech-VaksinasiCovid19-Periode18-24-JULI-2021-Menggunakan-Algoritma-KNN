from flask import Flask
from flaskext.mysql import MySQL
import config
import tweepy

app = Flask(__name__)

# Inisialisasi Konfigurasi MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = config.DATABASE_CONFIG['host']
app.config['MYSQL_DATABASE_USER'] = config.DATABASE_CONFIG['user']
app.config['MYSQL_DATABASE_PASSWORD'] = config.DATABASE_CONFIG['password']
app.config['MYSQL_DATABASE_DB'] = config.DATABASE_CONFIG['database']
mysql.init_app(app)

# Inisialisasi Konfigurasi Twitter API
auth = tweepy.OAuthHandler(config.TWITTER_API_CONFIG['api_key'], config.TWITTER_API_CONFIG['api_secret_key'])
auth.set_access_token(config.TWITTER_API_CONFIG['access_token'], config.TWITTER_API_CONFIG['access_token_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

from application import routes