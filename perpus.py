import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def cetak_df(df):
    df = pd.DataFrame(df)
    df['id'] = df.index
    kolom = df.columns.tolist()
    kolom.insert(0, kolom.pop())
    df = df[kolom]

    cetak = df.to_string(index=False)
    cetak = cetak.split('\n')

    for i in range(len(cetak)):
        cetak[i] = list(cetak[i])

    pemisah = []
    for i in range(len(cetak[0]) - 1):
        if cetak[0][i] != ' ' and cetak[0][i + 1] == ' ':
            pemisah.append(i + 1)

    pembatas = '╔'
    for i in range(len(cetak[0])):
        if i in pemisah:
            pembatas += '╦═'
        else:
            pembatas += '═'
    pembatas += '╗'

    pembatas_atas = pembatas
    pembatas_tengah = pembatas.replace('╔', '╠').replace('╦', '╬').replace('╗', '╣')
    pembatas_bawah = pembatas.replace('╔', '╚').replace('╦', '╩').replace('╗', '╝')

    print(pembatas_atas)
    awal = True
    for i in cetak:
        if awal:
            awal = False
        else:
            print(pembatas_tengah)

        for j in pemisah[::-1]:
            i.insert(j, '║')
        print('║' + ''.join(i) + '║')
    print(pembatas_bawah)

def baca_csv(nama_file):
    df = pd.read_csv(nama_file, index_col="id")
    return df

def tulis_csv(df, nama_file):
    df.to_csv(nama_file)

def get_last_id(df):
    if len(df.index) > 0:
        return df.index[-1]
    else:
        return 0

def authenticate(username, password):
    user_df = pd.read_csv('user.csv')

    users = user_df.values.tolist()
    for user in users:
        if user[0] == username and user[1] == password:
            return True
    return False

def anggota_baru():
    os.system('cls')
    nama_lengkap = input('Masukkan nama lengkap anggota: ')
    alamat_rumah = input('Masukkan alamat rumah anggota: ')
    nomor_telepon = input('Masukkan nomor telepon anggota: ')

    df = baca_csv('anggota.csv')
    df.loc[get_last_id(df) + 1] = [nama_lengkap, alamat_rumah, nomor_telepon]

    tulis_csv(df, 'anggota.csv')

    # Pause
    input('Berhasil! Tekan enter untuk melanjutkan')

def tampilkan_anggota():
    os.system('cls')
    df = baca_csv('anggota.csv')
    
    keyword = input('Masukkan nama anggota (kosongi untuk menampilkan semua): ')
    keyword = keyword.replace(' ', '|')

    if any(df['nama_lengkap'].str.contains(keyword, case=False)):
        cetak_df(df[
                df['nama_lengkap'].str.contains(keyword, case=False)
            ])

    else :
        print('Anggota tidak ditemukan')
    
    # Pause
    input('Tekan enter untuk melanjutkan')
    

def edit_anggota():
    os.system('cls')
    df = baca_csv('anggota.csv')

    id = int(input('Masukkan id anggota yang ingin diedit (angka): '))

    # Memastikan id anggota ada
    if id not in df.index:
        input(f'Anggota dengan id {id} tidak ditemukan!')
        return

    while True:
        os.system('cls')
        print('Mengedit anggota')
        print('[1] Nama lengkap: ' + df.loc[id, 'nama_lengkap'])
        print('[2] Alamat: ' + df.loc[id, 'alamat'])
        print('[3] Nomor telepon: ' + str(df.loc[id, 'no_tlp']))
        print('[4] Selesai')

        pilihan = input('Masukan: ')
        match pilihan:
            case '1':
                nama_lengkap_baru = input('Masukkan nama lengkap baru: ')
                df.loc[id, 'nama_lengkap'] = nama_lengkap_baru
            case '2':
                alamat_baru = input('Masukkan alamat baru: ')
                df.loc[id, 'alamat'] = alamat_baru
            case '3':
                no_tlp_baru = input('Masukkan nomor telepon baru: ')
                df.loc[id, 'no_tlp'] = int(no_tlp_baru)
            case '4':
                break
            case '_':
                input('Pilihan tidak valid! Tekan enter untuk melanjutkan')
                continue

        tulis_csv(df, 'anggota.csv')
        input('Berhasil! Tekan enter untuk melanjutkan')

def buku_baru():
    os.system('cls')
    judul = input('Masukkan judul buku: ')
    isbn = input('Masukkan ISBN buku: ')
    pengarang = input('Masukkan nama pengarang buku: ')
    penerbit = input('Masukkan nama penerbit buku: ')
    genre = input('Masukkan genre buku: ')
    bahasa = input('Masukkan bahasa buku: ')
    jml_salinan = int(input('Masukkan jumlah salinan buku (angka): '))

    df = baca_csv('buku.csv')
    df.loc[get_last_id(df) + 1] = [judul, isbn, pengarang, penerbit, genre, bahasa, jml_salinan]

    tulis_csv(df, 'buku.csv')

    # Pause
    input('Berhasil! Tekan enter untuk melanjutkan')

def tampilkan_buku():
    os.system('cls')
    df = baca_csv('buku.csv')

    keyword = input('Masukkan keyword buku (contoh: orwell 1984/kosongi untuk menampilkan semua): ')
    keyword = keyword.replace(' ', '|')
    if any(df['judul'].str.contains(keyword, case=False) | df['pengarang'].str.contains(keyword, case=False)):
        cetak_df(df[
                df['judul'].str.contains(keyword, case=False) |
                df['pengarang'].str.contains(keyword, case=False)
            ])
    else:
        print('\nBuku tidak tersedia')

    # Pause
    input('\nTekan enter untuk melanjutkan')

def edit_buku():
    os.system('cls')
    df = baca_csv('buku.csv')
    df['isbn'] = df['isbn'].astype(str)

    id = int(input('Masukkan id buku yang ingin diedit (angka): '))

    # Memastikan id buku ada
    if id not in df.index:
        input(f'Buku dengan id {id} tidak ditemukan!')
        return

    while True:
        os.system('cls')
        print('Mengedit buku')
        print('[1] Judul: ' + df.loc[id, 'judul'])
        print('[2] ISBN: ' + df.loc[id, 'isbn'])
        print('[3] Pengarang: ' + df.loc[id, 'pengarang'])
        print('[4] Penerbit: ' + df.loc[id, 'penerbit'])
        print('[5] Genre: ' + df.loc[id, 'genre'])
        print('[6] Bahasa: ' + df.loc[id, 'bahasa'])
        print('[7] Jumlah salinan: ' + str(df.loc[id, 'jml_salinan']))
        print('[8] Selesai')

        pilihan = input('Masukan: ')
        match pilihan:
            case '1':
                nama_lengkap_baru = input('Masukkan judul baru: ')
                df.loc[id, 'judul'] = nama_lengkap_baru
            case '2':
                isbn_baru = input('Masukkan ISBN baru: ')
                df.loc[id, 'isbn'] = isbn_baru
            case '3':
                pengarang_baru = input('Masukkan pengarang baru: ')
                df.loc[id, 'pengarang'] = pengarang_baru
            case '4':
                penerbit_baru = input('Masukkan penerbit baru: ')
                df.loc[id, 'penerbit'] = penerbit_baru
            case '5':
                genre_baru = input('Masukkan genre baru: ')
                df.loc[id, 'genre'] = genre_baru
            case '6':
                bahasa_baru = input('Masukkan bahasa baru: ')
                df.loc[id, 'bahasa'] = bahasa_baru
            case '7':
                jml_salinan_baru = input('Masukkan jumlah salinan baru (angka): ')
                df.loc[id, 'jml_salinan'] = int(jml_salinan_baru)
            case '8':
                break
            case '_':
                input('Pilihan tidak valid! Tekan enter untuk melanjutkan')
                continue

        tulis_csv(df, 'buku.csv')
        input('Berhasil! Tekan enter untuk melanjutkan')

def pinjaman_suatu_buku():
    os.system('cls')

    buku_df = baca_csv('buku.csv')

    id_buku = int(input('Masukkan id buku (angka): '))

    # Memastikan id buku ada
    if id_buku not in buku_df.index:
        input(f'Buku dengan id {id_buku} tidak ditemukan!')
        return

    pinjaman_df = baca_csv('peminjaman.csv')
    anggota_df = baca_csv('anggota.csv')

    print(f'Menampilkan riwayat pinjaman dari {buku_df.loc[id_buku, "judul"]}')
    print('')

    pinjaman_df = pinjaman_df[pinjaman_df['id_buku'] == id_buku]
    for index in pinjaman_df.index:
        nama_anggota = anggota_df.loc[pinjaman_df.loc[index, 'id_anggota'], 'nama_lengkap']
        print(f'Id pinjaman: {index}')
        print(f'Nama peminjam: {nama_anggota}')
        print(f'Tanggal meminjam: {pinjaman_df.loc[index, "tanggal_meminjam"]}')
        print(f'Tanggal pengembalian: {pinjaman_df.loc[index, "tanggal_pengembalian"]}')
        print('\n')

    input('Tekan enter untuk melanjutkan.')

def pinjaman_baru():
    os.system('cls')

    buku_df = baca_csv('buku.csv')
    anggota_df = baca_csv('anggota.csv')

    id_buku = int(input('Masukkan id buku (angka): '))

    # Memastikan id buku ada
    if id_buku not in buku_df.index:
        input(f'Buku dengan id {id_buku} tidak ditemukan!')
        return

    # Memastikan buku tersedia
    if buku_df.loc[id_buku, 'jml_salinan'] <= 0:
        input('Salinan buku tidak tersedia! Tekan enter untuk melanjutkan')
        return

    # Memastikan id anggota ada
    id_anggota = int(input('Masukkan id anggota peminjam (angka): '))
    if id_anggota not in anggota_df.index:
        input(f'Anggota dengan id {id_anggota} tidak ditemukan!')
        return

    tanggal_meminjam = input('Masukkan tanggal meminjam (contoh: 2023-04-20): ')
    tanggal_pengembalian = "Belum dikembalikan"
    
    buku_df.loc[id_buku, 'jml_salinan'] -= 1
    tulis_csv(buku_df, 'buku.csv')

    df = baca_csv('peminjaman.csv')
    df.loc[get_last_id(df) + 1] = [id_buku, id_anggota, tanggal_meminjam, tanggal_pengembalian]

    tulis_csv(df, 'peminjaman.csv')

    # Pause
    input('Berhasil! Tekan enter untuk melanjutkan')

def ubah_pinjaman():
    os.system('cls')
    df = baca_csv('peminjaman.csv')
    buku_df = baca_csv('buku.csv')
    anggota_df = baca_csv('anggota.csv')

    print('Menampilkan semua pinjaman yang belum selesai\n')
    for index in df[df['tanggal_pengembalian'] == 'Belum dikembalikan'].index:
        nama_anggota = anggota_df.loc[df.loc[index, 'id_anggota'], 'nama_lengkap']
        judul_buku = buku_df.loc[df.loc[index, 'id_buku'], 'judul']
        print(f'Id pinjaman: {index}')
        print(f'Nama peminjam: {nama_anggota}')
        print(f'Judul buku: {judul_buku}')
        print(f'Tanggal meminjam: {df.loc[index, "tanggal_meminjam"]}')
        print(f'Tanggal pengembalian: {df.loc[index, "tanggal_pengembalian"]}')
        print('\n')

    id_pinjaman = int(input('Masukkan id pinjaman (angka): '))

    # Memastikan id pinjaman ada
    if id_pinjaman not in df.index:
        input(f'Pinjaman dengan id {id_pinjaman} tidak ditemukan!')
        return

    tanggal_pengembalian = input('Masukkan tanggal pengembalian (contoh: 2023-04-20): ')

    buku_df.loc[df.loc[id_pinjaman, 'id_buku'], 'jml_salinan'] += 1
    df.loc[id_pinjaman, 'tanggal_pengembalian'] = tanggal_pengembalian

    tulis_csv(buku_df, 'buku.csv')
    tulis_csv(df, 'peminjaman.csv')

    # Pause
    input('Berhasil! Tekan enter untuk melanjutkan')

def hapus_pinjaman():
    os.system('cls')
    print('Apakah Anda yakin ingin menghapus semua data pinjaman yang sudah dikembalikan?')
    print('''
||======================================||
||               [1] Ya                 ||
||               [2] Tidak              ||
||======================================||
''')
    a = input('Masukan: ')
    if a == '1':
        df = baca_csv('peminjaman.csv')
        panjang_lama = len(df)

        df = df[df['tanggal_pengembalian'] == 'Belum dikembalikan']
        panjang_baru = len(df)

        tulis_csv(df, 'peminjaman.csv')
        input(f'{panjang_lama - panjang_baru} data berhasil dihapus! Tekan enter untuk melanjutkan')
    elif a == '2':
        return
    else:
        input('Pilihan tidak valid! Kembali ke menu awal')
        return

def init_pustakawan():
    while True:
        os.system('cls')
        pinjaman_df = baca_csv('peminjaman.csv')
        anggota_df = baca_csv('anggota.csv')
        buku_df = baca_csv('buku.csv')

        pinjaman_selesai = len(pinjaman_df[pinjaman_df['tanggal_pengembalian'] != 'Belum dikembalikan'])
        pinjaman_belum = len(pinjaman_df) - pinjaman_selesai
        anggota_terdaftar = len(anggota_df)
        jumlah_buku = len(buku_df)

        print(f'''
======================================
                 Halo                 
\t{anggota_terdaftar} anggota terdaftar\t\t
\t{jumlah_buku} buku berbeda tersedia\t\t
\t{pinjaman_selesai} pinjaman diselesaikan\t\t
\t{pinjaman_belum} buku belum dikembalikan\t
                                      
         Silahkan pilih opsi:         

         -- Anggota --
 [1] Tambahkan anggota baru           
 [2] Tampilkan anggota terdaftar      
 [3] Edit anggota terdaftar           

           -- Buku --
 [4] Tambahkan buku baru              
 [5] Tampilkan buku                   
 [6] Edit buku                        

           -- Pinjaman --
 [7] Tambahkan data pinjaman buku
 [8] Tampilkan riwayat pinjaman suatu buku
 [9] Ubah data pinjaman buku
 [10] Hapus data pinjaman yang telah dikembalikan

 [11] Kembali ke menu awal         
======================================
    ''')
        opsi = input('Masukan: ')
        match opsi:
            case '1':
                anggota_baru()
            case '2':
                tampilkan_anggota()
            case '3':
                edit_anggota()
            case '4':
                buku_baru()
            case '5':
                tampilkan_buku()
            case '6':
                edit_buku()
            case '7':
                pinjaman_baru()
            case '8':
                pinjaman_suatu_buku()
            case '9':
                ubah_pinjaman()
            case '10':
                hapus_pinjaman()
            case '11':
                break
            case _:
                input('Tolong pilih sesuai dengan tabel yang telah disediakan. Tekan enter untuk melanjutkan')

def keyword_buku():
    keyword = input('Masukkan keyword buku (contoh: orwell 1984): ')
    keyword = keyword.replace(' ', '|')
    
    df = baca_csv('buku.csv')
    if any(df['judul'].str.contains(keyword, case=False) | df['pengarang'].str.contains(keyword, case=False)):
        cetak_df(df[
                df['judul'].str.contains(keyword, case=False) |
                df['pengarang'].str.contains(keyword, case=False)
            ])
    else:
        print('\nBuku tidak tersedia')


    input('\nTekan enter untuk melanjutkan')

def init_pengunjung():
    while True:
        os.system('cls')
        print('''
||======================================||
||                 Halo                 ||
||        [1] Cari buku                 ||
||        [2] Kembali ke menu awal      ||
||======================================||
    ''')
        pilih = input ('Masukan: ')
        match pilih :
            case '1' :
                keyword_buku()
            case '2' :
                break
            case _:
                input('Tolong pilih sesuai dengan tabel yang telah disediakan. Tekan enter untuk melanjutkan')


while True :
    os.system('cls')
    print('''
||======================================||
||      Selamat datang di Libra.ly      ||
||  Silahkan pilih penggunaan aplikasi: ||
||                                      ||
||           [1] Pustakawan             ||
||           [2] Pengunjung             ||
||           [3] Akhiri Program         ||
||======================================||
''')

    pengguna = input('Masukan: ')
    match pengguna:
        case '1':
            while True:
                os.system('cls')
                username = input('Masukkan username: ')
                password = input('Masukkan password: ')

                if authenticate(username, password):
                    input('Autentikasi berhasil! Tekan enter untuk melanjutkan')
                    init_pustakawan()
                    break
                else:
                    print('Username atau password salah!')
                    print('''
||======================================||
||           [1] Coba lagi              ||
||           [2] Kembali                ||
||======================================||
''')
                    a = input('Masukan: ')
                    if a == '1':
                        continue
                    elif a == '2':
                        break
                    else:
                        input('Pilihan tidak valid! Kembali ke menu awal')
                        break
        case '2':
            init_pengunjung()
        case '3':
            input ('Program telah berakhir. Tekan enter untuk mengakhiri')
            break
        case _:
            input('Tolong pilih sesuai dengan tabel yang telah disediakan. Tekan enter untuk melanjutkan')
