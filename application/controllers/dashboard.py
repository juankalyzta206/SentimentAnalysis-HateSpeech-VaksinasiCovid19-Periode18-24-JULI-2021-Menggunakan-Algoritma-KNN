from application.models import Models
from flask import request

class DashboardController:

    def getData(self):
        # menyiapkan dict sebagai wadah
        data = {}

        # SELECT jumlah data crawling dari database
        instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_crawling')
        # input ke dalam dict
        data['data_crawling'] = instance_Model.select()[0]['jumlah']

        # SELECT jumlah data preprocessing dari database
        instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean')
        # input ke dalam dict
        data['data_preprocessing'] = instance_Model.select()[0]['jumlah']

        # SELECT jumlah data preprocessing dari database
        instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_clean WHERE sentiment_type IS NOT NULL')
        # input ke dalam dict
        data['data_berlabel'] = instance_Model.select()[0]['jumlah']

        # SELECT jumlah data preprocessing dari database
        instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_testing')
        # input ke dalam dict
        data['data_tes'] = instance_Model.select()[0]['jumlah']

        # SELECT jumlah data preprocessing dari database
        instance_Model = Models('SELECT COUNT(id) as jumlah FROM tbl_tweet_training')
        # input ke dalam dict
        data['data_latih'] = instance_Model.select()[0]['jumlah']

        # kembalikan data dengan dict yang berisi data-data yang telah diambil dari database
        return data