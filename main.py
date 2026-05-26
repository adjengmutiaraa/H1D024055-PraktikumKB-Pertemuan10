import random
import matplotlib.pyplot as plt

from InisiasiPopulasi import inisialisasi_populasi
from EvaluasiFitness import hitung_fitness
from selection import roulette_wheel_selection, tournament_selection
from crossover import one_point_crossover, two_point_crossover, uniform_crossover
from mutation import swap_mutation, inversion_mutation, uniform_mutation

# DATA BARANG (Sesuai Ketentuan Soal)
barang = [
    ("Barang1", 10, 5),
    ("Barang2", 40, 4),
    ("Barang3", 30, 6),
    ("Barang4", 50, 3),
    ("Barang5", 35, 7)
]

KAPASITAS_GUDANG = 15

def tentukan_metode_dari_nim(nim):
    # Ambil 2 digit terakhir dari NIM
    digits = []
    for char in nim:
        if char.isdigit():
            digits.append(int(char))
    
    if len(digits) < 2:
        raise ValueError("NIM harus memiliki setidaknya 2 digit angka")
    
    # Dua digit terakhir
    digit_seleksi = digits[-2]
    digit_crossover = digits[-1]
    
    # Penjumlahan untuk mutasi
    penjumlahan = digit_seleksi + digit_crossover
    digit_mutasi = penjumlahan % 10
    
    # Tentukan SELEKSI (berdasarkan digit_seleksi)
    if digit_seleksi % 2 == 0:
        seleksi = "RWS"
    else:
        seleksi = "TS"
    
    # Tentukan CROSSOVER (berdasarkan digit_crossover)
    if digit_crossover % 3 == 0:
        crossover = "One Point"
    elif digit_crossover % 3 == 1:
        crossover = "Two Point"
    else:
        crossover = "Uniform"
    
    # Tentukan MUTASI (berdasarkan digit_mutasi)
    if digit_mutasi % 3 == 0:
        mutasi = "Swap"
    elif digit_mutasi % 3 == 1:
        mutasi = "Inversion"
    else:
        mutasi = "Uniform"
    
    return seleksi, crossover, mutasi, digit_seleksi, digit_crossover, digit_mutasi, penjumlahan

def pilih_seleksi(populasi, fitness_populasi, metode):
    if metode == "RWS":
        return roulette_wheel_selection(populasi, fitness_populasi)
    else:
        return tournament_selection(populasi, fitness_populasi, k=3)

def pilih_crossover(parent1, parent2, metode):
    if metode == "Two Point":
        return two_point_crossover(parent1, parent2)
    elif metode == "Uniform":
        return uniform_crossover(parent1, parent2)
    else:
        return one_point_crossover(parent1, parent2)

def pilih_mutasi(kromosom, prob_mutasi, metode):
    if random.random() < prob_mutasi:
        if metode == "Swap":
            return swap_mutation(kromosom)
        elif metode == "Uniform":
            return uniform_mutation(kromosom)
        else:
            return inversion_mutation(kromosom)
    return kromosom

def run_ga(jumlah_generasi, jumlah_populasi, prob_crossover, prob_mutasi, 
          seleksi_metode, crossover_metode, mutasi_metode):
    
    jumlah_gen = len(barang)
    populasi = inisialisasi_populasi(jumlah_populasi, jumlah_gen)
    
    best_fitness_list = []
    worst_fitness_list = []
    avg_fitness_list = []
    all_fitness = []
    
    best_individu = None
    best_fitness_overall = 0
    
    for generasi in range(jumlah_generasi):
        fitness_populasi = [hitung_fitness(individu, barang, KAPASITAS_GUDANG) for individu in populasi]
        
        best_fitness = max(fitness_populasi)
        worst_fitness = min(fitness_populasi)
        avg_fitness = sum(fitness_populasi) / len(fitness_populasi)
        
        best_fitness_list.append(best_fitness)
        worst_fitness_list.append(worst_fitness)
        avg_fitness_list.append(avg_fitness)
        all_fitness.append(fitness_populasi.copy())
        
        if best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            index_best = fitness_populasi.index(best_fitness)
            best_individu = populasi[index_best].copy()
        
        new_populasi = []
        used_indices = []
        
        while len(new_populasi) < jumlah_populasi:
            parent1, idx1 = pilih_seleksi(populasi, fitness_populasi, seleksi_metode)
            used_indices.append(idx1)
            
            available_indices = [i for i in range(len(populasi)) if i not in used_indices]
            if not available_indices:
                used_indices = [idx1]
                available_indices = [i for i in range(len(populasi)) if i != idx1]
            
            parent2, idx2 = pilih_seleksi(
                [populasi[i] for i in available_indices],
                [fitness_populasi[i] for i in available_indices],
                seleksi_metode
            )
            used_indices.append(available_indices[idx2])
            
            if random.random() < prob_crossover:
                anak1, anak2 = pilih_crossover(parent1, parent2, crossover_metode)
            else:
                anak1, anak2 = parent1[:], parent2[:]
            
            anak1 = pilih_mutasi(anak1, prob_mutasi, mutasi_metode)
            anak2 = pilih_mutasi(anak2, prob_mutasi, mutasi_metode)
            
            new_populasi.extend([anak1, anak2])
        
        populasi = new_populasi[:jumlah_populasi]
    
    # Grafik
    plt.figure(figsize=(12, 7))
    
    for i in range(jumlah_generasi):
        x = [i + 1] * len(all_fitness[i])
        y = all_fitness[i]
        plt.scatter(x, y, color='gray', alpha=0.1, s=20)
    
    plt.plot(range(1, jumlah_generasi + 1), best_fitness_list, 
             color='blue', linewidth=2, label='Fitness Tertinggi')
    plt.plot(range(1, jumlah_generasi + 1), worst_fitness_list, 
             color='orange', linewidth=2, label='Fitness Terendah')
    plt.plot(range(1, jumlah_generasi + 1), avg_fitness_list, 
             color='red', linewidth=2, label='Fitness Rata-rata')
    
    plt.title(f'Perkembangan Nilai Fitness\nSeleksi={seleksi_metode} | Crossover={crossover_metode} | Mutasi={mutasi_metode}')
    plt.xlabel('Generasi')
    plt.ylabel('Nilai Fitness (Keuntungan)')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    total_keuntungan = hitung_fitness(best_individu, barang, KAPASITAS_GUDANG)
    total_ukuran = sum([barang[i][2] for i in range(len(best_individu)) if best_individu[i] == 1])
    
    selected_items = []
    for i in range(len(best_individu)):
        if best_individu[i] == 1:
            selected_items.append(barang[i][0])
    
    return total_keuntungan, total_ukuran, selected_items

# PROGRAM UTAMA
if __name__ == "__main__":
    nim = input("Masukkan NIM Anda (Cth: H1D023110): ").strip()
    
    seleksi, crossover, mutasi, dig_seleksi, dig_crossover, dig_mutasi, penjumlahan = tentukan_metode_dari_nim(nim)
    
    print("\nHASIL PENENTUAN METODE")
    print(f"NIM: {nim}")
    print(f"Dua digit terakhir NIM: {dig_seleksi}{dig_crossover}")
    print(f"Digit untuk Seleksi: {dig_seleksi}")
    print(f"Digit untuk Crossover: {dig_crossover}")
    print(f"Penjumlahan: {dig_seleksi} + {dig_crossover} = {penjumlahan}")
    print(f"Digit terakhir penjumlahan untuk Mutasi: {dig_mutasi}")
    print()
    print(f"Seleksi (dari digit {dig_seleksi}): {seleksi}")
    print(f"Crossover (dari digit {dig_crossover}): {crossover}")
    print(f"Mutasi (dari digit {dig_mutasi}): {mutasi}")
    
    JUMLAH_GENERASI = 50
    JUMLAH_POPULASI = 20
    PROB_CROSSOVER = 0.7
    PROB_MUTASI = 0.1
    
    print("\nMenjalankan Algoritma Genetika...")
    
    keuntungan, ukuran, barang_terpilih = run_ga(
        jumlah_generasi=JUMLAH_GENERASI,
        jumlah_populasi=JUMLAH_POPULASI,
        prob_crossover=PROB_CROSSOVER,
        prob_mutasi=PROB_MUTASI,
        seleksi_metode=seleksi,
        crossover_metode=crossover,
        mutasi_metode=mutasi
    )
    
    print("\nHASIL OPTIMASI KNAPSACK")
    print(f"Kapasitas Maksimal Gudang: {KAPASITAS_GUDANG}")
    print(f"Total Keuntungan Maksimal: {keuntungan}")
    print(f"Total Ukuran Terpakai: {ukuran}")
    print(f"Sisa Kapasitas Gudang: {KAPASITAS_GUDANG - ukuran}")
    print("\nBarang yang Dibeli:")
    for item in barang_terpilih:
        print(f"  - {item}")