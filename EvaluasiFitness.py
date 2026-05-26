# Fungsi untuk menghitung nilai fitness
def hitung_fitness(kromosom, barang, kapasitas_gudang):
    total_keuntungan = 0
    total_ukuran = 0
    
    for i in range(len(kromosom)):
        if kromosom[i] == 1:
            total_keuntungan += barang[i][1]  # keuntungan
            total_ukuran += barang[i][2]      # ukuran
    
    if total_ukuran > kapasitas_gudang:
        return 0  # Penalti jika melebihi kapasitas
    else:
        return total_keuntungan