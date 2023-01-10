from math import sqrt
import itertools

class KNearestNeighbors:
    def __init__(self, k, model_latih):
        self.nilai_k = k  # deklarasi & inisialisasi nilai k tetangga terdekat
        self.model_latih = model_latih  # deklarasi & inisialisasi model_latih
    
    # Fungsi utama untuk memprediksi label data (sentimen)
    def predict_labelList(self, vector_uji):

        vector_latih = self.model_latih['vector_list']
        label_latih = self.model_latih['label_list']

        # wadah untuk menampung nilai label dari keseluruhan data uji
        label_prediction = []
        # wadah untuk menampung nilai probabilitas dari label prediksi
        prob_prediction = []
        # wadah untuk menampung nilai jarak tetangga terdekat
        near_neighbors = []
        # wadah untuk menampung nilai tetangga terdekat
        sent_neighbors = []
        # wadah untuk menampung teks tetangga terdekat
        teks_neighbors = []

        print('\n-- PROSES '+ str(len(vector_uji)) +' DATA --')	# PRINT KE CMD
        # Berulang sebanyak jumlah data uji
        for i in range(len(vector_uji)):
            distance = ''
            nearest_neighbors = ''
            sentiment_neighbors = ''
            prob_NONHS = 0
            prob_HS = 0
            sentiment_prediction = 0

            # START
            # 1. Menghitung jarak antar data untuk tiap data uji (berdasarkan nilai i)
            distance = self.euclidean_distance(vector_uji[i], vector_latih)
            # 2. Mencari k tetangga terdekat berdasarkan nilai distance
            nearest_neighbors = self.nearest_neighbors(distance)
            # 3. Cek label dari k tetangga terdekat berdasarkan label_latih
            sentiment_neighbors = self.sentiment_neighbors(nearest_neighbors, label_latih)
            # 4. Mencari probabilitas untuk label k tetangga terdekat
            prob_NONHS, prob_HS = self.probability_neighbors(sentiment_neighbors)
            # 5. Mencari probabilitas yang dominan untuk mendapatkan nilai sentimen dari k tetangga terdekat (voting)
            if prob_NONHS > prob_HS:
                sentiment_prediction = 'NONHS'
                prob_prediction.append(round(prob_NONHS*100, 2))
            else:
                sentiment_prediction = 'HS'
                prob_prediction.append(round(prob_HS*100, 2))
            # END

            # Menyimpan data prediksi untuk dikembalikan
            label_prediction.append(sentiment_prediction)
            near_neighbors.append(list(nearest_neighbors.values()))
            sent_neighbors.append(sentiment_neighbors)
            teks_neighbors.append(self.get_textNeighbors(nearest_neighbors))
            print(str(i+1) +' / '+ str(len(vector_uji)))	# PRINT KE CMD
        print('\n-- SELESAI --\n')	# PRINT KE CMD

        data_dict = {
            'label_prediction' : label_prediction, 
            'prob_prediction' : prob_prediction, 
            'near_neighbors' : near_neighbors, 
            'sent_neighbors' : sent_neighbors, 
            'teks_neighbors' : teks_neighbors,
            'k' : self.nilai_k 
        }

        return data_dict
    
    # Fungsi untuk menghitung jarak dengan metrik jarak euclidean distance
    def euclidean_distance(self, vector_uji, vector_latih):
        # wadah untuk menampung nilai jarak
        distance = {}

        # Euclidean distance = sqrt( (x1 - x2)^2 + (y1 - y2)^2 + (z1 - z2)^2 + .... )
        for i in range(len(vector_latih)):
            total = 0
            for j in range(len(vector_uji)):
                total += pow((vector_uji[j]-vector_latih[i][j]), 2)
            distance[i] = sqrt(total)
        return distance
    # Fungsi untuk mencari K tetangga terdekat
    def nearest_neighbors(self, distance):

        K =  self.nilai_k

        # mencari K tetangga terdekat berdasarkan value dari dict distance
        neighbors_sortASC = dict(sorted(distance.items(), key=lambda item: item[1]))
        # mendapatkan dict sebanyak nilai K
        nearest_neighbors = dict(itertools.islice(neighbors_sortASC.items(), K))

        return nearest_neighbors
        
    # Fungsi untuk mencari nilai label sentimen dari k tetangga terdekat
    def sentiment_neighbors(self, nearest_neighbors, label_latih):
        # membuat key dari dict menjadi isi list index_nearestNeighbors
        index_nearestNeighbors = list(nearest_neighbors)

        sentiment_neighbors = []
        # mendapatkan index dari list k tetangga terdekat berdasarkan list index_nearestNeighbors
        for index in index_nearestNeighbors:
            sentiment_neighbors.append(label_latih[index])

        return sentiment_neighbors
    
    def probability_neighbors(self, sentiment_neighbors):
        count_NONHS = 0
        count_HS = 0

        # menghitung jumlah NONHS dalam k tetangga terdekat
        for sentiment in sentiment_neighbors:
            if sentiment == 'NONHS':
                count_NONHS += 1
            else:
                count_HS +=1
        
        # mencari probabilitasnya
        prob_NONHS = count_NONHS / len(sentiment_neighbors)
        prob_HS = count_HS / len(sentiment_neighbors)

        return prob_NONHS, prob_HS

    def get_textNeighbors(self, nearest_neighbors):
        # membuat key dari dict menjadi isi list index_nearestNeighbors
        index_nearestNeighbors = list(nearest_neighbors)

        teks = []
        # mendapatkan index dari list k tetangga terdekat berdasarkan list index_nearestNeighbors
        for index in index_nearestNeighbors:
            teks.append(self.model_latih['teks_list'][index])
        return teks
