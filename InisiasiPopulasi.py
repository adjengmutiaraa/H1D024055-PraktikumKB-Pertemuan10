import random

# Fungsi untuk inisialisasi populasi
def inisialisasi_populasi(jumlah_populasi, jumlah_gen):
    populasi = []
    for i in range(jumlah_populasi):
        # Membuat kromosom dengan gen biner secara acak
        kromosom = [random.randint(0, 1) for _ in range(jumlah_gen)]
        populasi.append(kromosom)
    return populasi