from sqlalchemy import insert
from script.preprocess.preprocessing import clean_data
# from preprocess.mapping_location import add_location_data
import pandas as pd
import datetime
import time

def main_process(df):
    # Filter data dan hapus duplikasi
    df = df[(df['tipe_properti'] == 'Rumah') & (df['tipe_iklan'] == 'Dijual')]
    df.drop_duplicates(keep='first', inplace=True)

    # Ambil kecamatan unik
    df['kecamatan'] = df['kecamatan'].str.split(',').str[0]
    df = df[df.kecamatan != 'Sidoarjo']

    unique_kecamatan = pd.DataFrame(df['kecamatan'].unique(), columns=['Kecamatan'])

    # Load unique_location
    unique_location = pd.read_csv('./script/preprocess/location_1.csv')

    # Gabungkan data lokasi dengan data utama
    df = df.merge(unique_location, left_on='kecamatan', right_on='kecamatan', how='left')
    kecamatan = df.kecamatan.values
    df.drop(columns=['Unnamed: 0'], inplace=True)

    # Bersihkan data
    cleaned_df = clean_data(df)
    cleaned_df['kecamatan_1'] = kecamatan
    cleaned_df = cleaned_df.merge(unique_location, left_on='kecamatan_1', right_on='kecamatan', how='left', suffixes=('', '_unique'))
    cleaned_df.drop(columns=['distance_gerbangtol_unique','distance_school_unique','distance_hospital_unique','distance_tokoobat_unique', 'Unnamed: 0', 'kecamatan_unique'], inplace=True)

    return cleaned_df
def miss_handler(df):
    desired_columns = [
        'judul', 'harga', 'kecamatan', 'link', 'kamar_tidur', 'kamar_mandi',
        'luas_tanah', 'luas_bangunan', 'carport', 'sertifikat', 'daya_listrik',
        'kamar_pembantu', 'kamar_mandi_pembantu', 'dapur', 'ruang_makan',
        'ruang_tamu', 'kondisi_perabotan', 'jumlah_lantai', 'hadap',
        'konsep_dan_gaya_rumah', 'pemandangan', 'terjangkau_internet',
        'lebar_jalan', 'tahun_dibangun', 'tahun_di_renovasi', 'sumber_air',
        'hook', 'kondisi_properti', 'garasi', 'distance_gerbangtol',
        'distance_school', 'distance_hospital', 'distance_tokoobat',
        'bata_hebel', 'bata_merah', 'batako', 'beton', 'granit', 'keramik',
        'marmer', 'ubin', 'vinyl', 'ac', 'akses_parkir', 'balcony',
        'built_in_robes', 'cctv', 'golf_view', 'jalur_telepon', 'jogging_track',
        'keamanan', 'kitchen_set', 'kolam_ikan', 'kolam_renang',
        'lapangan_basket', 'lapangan_bola', 'lapangan_bulu_tangkis',
        'lapangan_tenis', 'lapangan_voli', 'masjid', 'one_gate_system',
        'pemanas_air', 'separate_dining_room', 'taman', 'tempat_gym',
        'tempat_jemuran', 'tempat_laundry', 'wastafel', 'kecamatan_1',
        'latitude', 'longitude'
    ]

    for col in desired_columns:
        if col not in df.columns:
            df[col] = 0
    # Urutkan kolom sesuai daftar kolom yang diinginkan
    df = df[desired_columns]

    return df

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def main(connection, log, engine):
    start = time.time()
    log_handler(connection, log, 'Fetching Data...')
    df = pd.read_sql('users_properti', con=engine)

    log_handler(connection, log, 'Processing Data...')
    data = main_process(df)
    final_data = miss_handler(data)

    log_handler(connection, log, 'Export Data...')
    final_data.to_sql('users_training', con=engine, index=False, if_exists='append')

    stop = time.time()
    log_handler(connection, log, f'Process Complete on: {stop - start}')

if __name__ == '__main__':
    main()
