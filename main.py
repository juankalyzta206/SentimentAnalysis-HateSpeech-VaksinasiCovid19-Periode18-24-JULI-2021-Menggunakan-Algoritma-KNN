from application import app

#Menjalankan program utama
if __name__ == "__main__":
	app.secret_key = 'KKP101'
	app.run(debug=True, use_reloader=True)