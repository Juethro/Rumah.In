from sqlalchemy import insert
# from preprocess.preprocessing import clean_data
# from preprocess.mapping_location import add_location_data
import pandas as pd
import datetime
import time

def main_process(df):
    # Filter data dan hapus duplikasi
    df = df[(df['Tipe Properti'] == 'Rumah') & (df['Tipe Iklan'] == 'Dijual')]
    df.drop_duplicates(keep='first', inplace=True)

    # Ambil kecamatan unik
    df['kecamatan'] = df['kecamatan'].str.split(',').str[0]
    df = df[df.kecamatan != 'Sidoarjo']

    unique_kecamatan = pd.DataFrame(df['kecamatan'].unique(), columns=['Kecamatan'])

    # Tambahkan data lokasi
    unique_location = add_location_data(df, unique_kecamatan)
    lat = unique_location.Latitude
    long = unique_location.Longitude
    unique_location.to_csv('location.csv', index=False)

    # Gabungkan data lokasi dengan data utama
    df = df.merge(unique_location, left_on='kecamatan', right_on='Kecamatan', how='left')
    kecamatan = df.kecamatan.values
    df.drop(columns=['Kecamatan'], inplace=True)

    # Bersihkan data
    cleaned_df = clean_data(df)
    cleaned_df['Kecamatan'] = kecamatan
    cleaned_df = cleaned_df.merge(unique_location, left_on='Kecamatan', right_on='Kecamatan', how='left')
    cleaned_df.drop(columns=['Distance_GerbangTol_y','Distance_School_y','Distance_Hospital_y','Distance_TokoObat_y'], inplace=True)

    return cleaned_df

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def main(connection, log, engine):
    start = time.time()
    log_handler(connection, log, 'Fetching Data...')
    df = pd.read_sql('users_properti', con=engine)

    log_handler(connection, log, 'Processing Data...')

    log_handler(connection, log, 'Export Data...')

    stop = time.time()
    log_handler(connection, log, f'Process Complete on: {stop - start}')

if __name__ == '__main__':
    main()
