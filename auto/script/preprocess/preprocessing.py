import pandas as pd
from sklearn.preprocessing import LabelEncoder
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
        return pd.to_numeric(area_str.replace('m²', '').strip(), errors='coerce')
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
    le = LabelEncoder()
    for col in columns:
        if df[col].dtype == 'object':
            df[col] = le.fit_transform(df[col].astype(str))

    numeric_cols = df.select_dtypes(include='number').columns
    median_values = df[numeric_cols].median()
    df = df.fillna(median_values)
    df.bfill(inplace=True)
    df.ffill(inplace=True)
    return df

def clean_data(df):
    df = df[(df['Tipe Properti'] == 'Rumah') & (df['Tipe Iklan'] == 'Dijual')]
    df.drop_duplicates(keep='first', inplace=True)
    df = df[df.kecamatan != 'Sidoarjo']

    drop_columns = ['judul', 'link', 'last_update', 'ID Iklan', 'deskripsi', 'luas tanah', 'luas bangunan', 
                    'Tipe Properti', 'Nomor Lantai', 'Tipe Iklan','cicilan','Latitude','Longitude']
    df.drop(columns=drop_columns, inplace=True)

    df['harga'] = df['harga'].apply(convert_price_to_number)
    df['Luas Bangunan'] = df['Luas Bangunan'].apply(convert_area_to_number)
    df['Luas Tanah'] = df['Luas Tanah'].apply(convert_area_to_number)
    df['Daya Listrik'] = df['Daya Listrik'].apply(convert_power_to_number)
    df['Lebar Jalan'] = df['Lebar Jalan'].apply(convert_width_to_number)

    for col in ['Material Bangunan', 'Material Lantai']:
        dummies = df[col].str.get_dummies(sep=', ')
        df = pd.concat([df, dummies], axis=1)
        df.drop(columns=[col], inplace=True)

    df['Kondisi Properti'] = df['Kondisi Properti'].replace('Bagus Sekali', 'Bagus')
    df['kecamatan'] = df['kecamatan'].str.split(',').str[0]
    df = df[df.kecamatan != 'Sidoarjo']

    label_columns = ['Sertifikat', 'Ruang Makan', 'Ruang Tamu', 'Kondisi Perabotan', 'Hadap', 
                     'Konsep dan Gaya Rumah', 'Pemandangan', 'Terjangkau Internet', 'Sumber Air', 
                     'Hook', 'Kondisi Properti', 'kecamatan']
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
    
    facilities = df['fasilitas'].str.get_dummies(sep=', ')
    df = pd.concat([df, facilities], axis=1)
    df.drop(columns=['fasilitas'], inplace=True)

    return df
