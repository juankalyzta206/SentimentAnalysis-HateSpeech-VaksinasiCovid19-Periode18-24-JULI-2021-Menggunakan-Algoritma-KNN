from application.models import Models
from flask import request, session, flash

class AuthController:

    def register(self):

        username = request.form['username'].strip()
        kata_sandi = request.form['kata_sandi'].strip()
        fullname = request.form['fullname'].strip()

        # cek record (ada?)
        instance_Model = Models('SELECT password, fullname FROM tbl_users WHERE username = %s')
        user = instance_Model.select_row(username)

        # record TIDAK ditemukan
        if user == None:
            data_tambah = (username, 'textmining_'+ str(kata_sandi) +'_sentimentanalysis', fullname)
            # simpan data user
            instance_Model = Models('INSERT INTO tbl_users(username, password, fullname) VALUES (%s, %s, %s)')
            instance_Model.query_sql(data_tambah)
            flash('Berhasil mendaftar, silakan masuk.', 'success')
            return True
        flash('Username telah terdaftar.', 'error')
        return False
    
    def login(self):

        username = request.form['username'].strip()
        kata_sandi = request.form['kata_sandi'].strip()
        
        # cek record (ada?)
        instance_Model = Models('SELECT password, fullname FROM tbl_users WHERE username = %s')
        user = instance_Model.select_row(username)

        # record ditemukan
        if user != None:
            # cek kecocokan kata sandi
            if 'textmining_'+ str(kata_sandi) +'_sentimentanalysis' == list(user)[0]:
                # session['username'] = username
                session['fullname'] = list(user)[1]
                return True
            flash('Username atau Kata Sandi tidak sesuai.')
            return False
        flash('Username tidak terdaftar.')
        return False
    
    def logout(self):
        if 'fullname' in session:
            # session.pop('username', None)   # menghapus sesi masuk user
            session.pop('fullname', None)   # menghapus sesi masuk user
        return None