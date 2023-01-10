class Vectorizer:
    def __init__(self, teks_list, label_list):
        self.teks_list = teks_list  # deklarasi & inisialisasi list teks yang akan dijadikan vektor
        self.label_list = label_list    # deklarasi & inisialisasi label dari teks list
    
    # Fungsi utama untuk membuat vektor angka berdasarkan list teks
    def create_vectorList(self):

        # Membuat list kata berdasarkan parameter self.teks_list
        text_word = self.get_wordList(self.teks_list)

        # Mencari fitur atau membuat list kata unik berdasarkan parameter text_word
        unique_words = self.get_uniqueWords(text_word)

        # Membuat vektor 0 dengan panjang = banyaknya fitur (unique_words) dan lebar = banyaknya list teks
        vector_listZero = self.get_zeroVector(len(unique_words), len(self.teks_list))

        # Membuat vektor angka dengan merubah vektor 0 berdasarkan frekuensi katanya
        vector_list = self.get_vectorList(vector_listZero, self.teks_list, unique_words)
        
        data_dict = {
            "teks_list" : self.teks_list,
            "label_list" : self.label_list,
            "unique_words" : unique_words,
            "vector_list" : vector_list,
        }
        return data_dict
        
    # mendapatkan list dari data uji berdasarkan model latih yang dipilih
    def test_vectorList(self, model):
        # Membuat vektor 0 dengan panjang = banyaknya fitur (unique_words) dan lebar = banyaknya list_teksUji
        vector_listZero = self.get_zeroVector(len(model['unique_words']), len(self.teks_list))

        # Membuat vektor angka dengan merubah vektor 0 berdasarkan frekuensi katanya
        vector_list = self.get_vectorList(vector_listZero, self.teks_list, model['unique_words'])
        return vector_list
    
    # Fungsi untuk memecah list teks menjadi list per kata
    def get_wordList(self, text_list):
        text_word = []
        for text in text_list:
            for word in text.split():
                text_word.append(word)
        return text_word
    
    # Fungsi untuk mencari kata unik (fitur) pada list per kata
    def get_uniqueWords(self, text_word) :
        unique_words = [] 
        for word in text_word:
            if not word in unique_words:
                unique_words.append(word)
        return unique_words
    
    # membuat vektor 0 dengan panjang = len(unique_words) & lebar = len(text_list)
    def get_zeroVector(self, panjang, lebar):
        vector_listZero = [[0 for i in range(panjang)] for j in range(lebar)]
        return vector_listZero

    # Membuat list vector
    def get_vectorList(self, vector_list, text_list, unique_words):
        for i, text in enumerate(text_list):
            for word in text.split():
                for j, unique in enumerate(unique_words):
                    if word == unique:
                        vector_list[i][j] += 1
        return vector_list