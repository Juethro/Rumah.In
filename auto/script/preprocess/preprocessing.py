import pandas as pd
import pickle
import numpy as np

def convert_price_to_number(price_str):
    price_str = price_str.replace('Rp ', '').replace('.', '').replace(',', '.')
    if 'Miliar' in price_str:
        return float(price_str.replace(' Miliar', '')) * 1e9
    elif 'Juta' in price_str:
        return float(price_str.replace(' Juta', '')) * 1e6
    return float(price_str)

def convert_area_to_number(area_str):
    if isinstance(area_str, str):
        return pd.to_numeric(area_str.replace('sqm', '').strip(), errors='coerce')
    return area_str

def convert_power_to_number(power_str):
    if isinstance(power_str, str):
        if 'Lainnya' in power_str:
            return None
        return pd.to_numeric(power_str.replace('Watt', '').strip(), errors='coerce')
    return power_str

def convert_width_to_number(width_str):
    if isinstance(width_str, str):
        return pd.to_numeric(width_str.replace('Mobil', '').strip(), errors='coerce')
    return width_str

def encode_and_fillna(df, columns):
    numeric_cols = df.select_dtypes(include='number').columns
    median_values = df[numeric_cols].median()
    df = df.fillna(median_values)
    df.bfill(inplace=True)
    df.ffill(inplace=True)

    for col in columns:
        with open(f'./auto/script/preprocess/labelencoder/label_encoder_{col}.pkl', 'rb') as f:
            le = pickle.load(f)
            df[col] = le.transform(df[col].astype(str))
    return df

def clean_data(df):
    df = df[(df['tipe_properti'] == 'Rumah') & (df['tipe_iklan'] == 'Dijual')]
    df.drop_duplicates(keep='first', inplace=True)
    df = df[df.kecamatan != 'Sidoarjo']

    drop_columns = ['last_update', 'id_iklan', 'deskripsi', 'luas_tanah_front', 'luas_bangunan_front', 
                    'tipe_properti', 'nomor_lantai', 'tipe_iklan','cicilan','latitude','longitude']
    df.drop(columns=drop_columns, inplace=True)

    df['harga'] = df['harga'].apply(convert_price_to_number)
    df['luas_bangunan'] = df['luas_bangunan'].apply(convert_area_to_number)
    df['luas_tanah'] = df['luas_tanah'].apply(convert_area_to_number)
    df['daya_listrik'] = df['daya_listrik'].apply(convert_power_to_number)
    df['lebar_jalan'] = df['lebar_jalan'].apply(convert_width_to_number)

    for col in ['material_bangunan', 'material_lantai']:
        dummies = df[col].str.get_dummies(sep=', ').rename(columns=lambda x: x.lower().replace(' ', '_'))
        df = pd.concat([df, dummies], axis=1)
        df.drop(columns=[col], inplace=True)

    df['kondisi_properti'] = df['kondisi_properti'].replace('Bagus Sekali', 'Bagus')
    df['kecamatan'] = df['kecamatan'].str.split(',').str[0]
    df = df[df.kecamatan != 'Sidoarjo']

    label_columns = ['sertifikat', 'ruang_makan', 'ruang_tamu', 'kondisi_perabotan', 'hadap', 
                        'konsep_dan_gaya_rumah', 'pemandangan', 'terjangkau_internet', 'sumber_air', 
                        'hook', 'kondisi_properti', 'kecamatan']
    
    df = encode_and_fillna(df, label_columns)

    mapping = {
        'golf view graha family hole no 1': 'Golf View',
        'Track Lari': 'Jogging Track',
        'Mesin Cuci': 'Tempat Laundry',
        'Kompor': 'Kitchen Set',
        'Kulkas': 'Kitchen Set',
        'Playground': 'Taman',
        'Keamanan 24 jam': 'Keamanan',
        'Ac':'AC'
    }
    for key, value in mapping.items():
        df['fasilitas'] = df['fasilitas'].str.replace(key, value)

    facilities = df['fasilitas'].str.get_dummies(sep=', ').rename(columns=lambda x: x.lower().replace(' ', '_'))
    df = pd.concat([df, facilities], axis=1)
    df.drop(columns=['fasilitas'], inplace=True)


    return df
