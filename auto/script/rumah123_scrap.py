import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from tqdm import tqdm
from sqlalchemy import insert
import datetime

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)


def get_first_data(driver, page, connection, log):
    data = {
        "judul" : [],
        "harga" : [],
        "cicilan" : [],
        "kecamatan" : [],
        "luas_tanah_front" : [],
        "luas_bangunan_front" : [],
        "link" : [],
        "images_link" : []
    }
    for i in tqdm(range(page), desc="Get Cover Data"):
        url = f'https://www.rumah123.com/jual/cari/?location=surabaya&page={i+1}'
        try:
            driver.set_page_load_timeout(10)
            driver.get(url)
        except TimeoutException:
            log_handler(connection, log, f'Timeout...{i}')
            continue
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        images_class = soup.find_all(class_="ui-organism-intersection__element intersection-card-container")
        section_class = soup.find_all(class_="card-featured__middle-section")
        for section, image in zip(section_class, images_class):
            data["images_link"].append(image.find("img").get('src'))
            data["judul"].append(section.find("h2").get_text())
            data["harga"].append(section.find("strong").get_text())
            data["cicilan"].append(section.find("em").get_text())
            data["kecamatan"].append([kecamatan.get_text() for kecamatan in section.find_all("span") if "Surabaya" in kecamatan.get_text()][0])
            data["luas_tanah_front"].append(section.find_all(class_ = "attribute-info")[0].get_text().replace("LT : ", ""))
            try:
                data["luas_bangunan_front"].append(section.find_all(class_ = "attribute-info")[1].get_text().replace("LB : ", ""))
            except:
                data["luas_bangunan_front"].append("")
            data["link"].append(section.a["href"])
        time.sleep(3)

    df = pd.DataFrame(data)
    return df

def get_all_data(df_cover, driver, connection, log):
    extension_links = df_cover["link"].tolist()
    save_list = []
    for i, extension in tqdm(enumerate(extension_links), desc="Get All Data"):
        try:
            data_full = {
                "link" : extension,
                "fasilitas" : []
            }
            url = f'https://www.rumah123.com{extension}'
            try:
                driver.set_page_load_timeout(10)
                driver.get(url)
            except TimeoutException:
                log_handler(connection, log, f'Timeout...{i}')
                continue
            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            last_update = soup.find_all(class_ = "r123-listing-summary__header-container-updated")
            data_full["last_update"] = last_update[0].get_text()
            items = soup.find_all(class_ = "listing-specification-v2__item-label")
            values = soup.find_all(class_ = "listing-specification-v2__item-value")
            for item, value in zip (items, values):
                data_full[item.get_text().lower().replace(" ", "_")] = value.get_text()
            desc = soup.find(class_ = "ui-atomic-text ui-atomic-text--styling-default ui-atomic-text--typeface-primary content-wrapper").get_text()
            data_full["deskripsi"] = desc
            data_full["fasilitas"] = ", ".join([fasilitas.get_text().strip() for fasilitas in soup.find_all(class_ = "ui-facilities-portal__text")])
            save_list.append(data_full)
            time.sleep(3)
        except Exception as e:
            """
            error udah dicheck dia emang di beberapa tempat kalo diclick return ke halaman yang bukan dituju
            tapi malah ke link https://www.rumah123.com/jual/surabaya/rumah/ seharusnya bug dari web-nya.
            """
            print(e)
            log_handler(connection, log, f'error di link {extension} dengan error:')
            time.sleep(10)
    return save_list

def miss_handler_n_filter(df, scraped_link):
    desired_columns = ['judul', 'harga', 'cicilan', 'kecamatan', 'luas_tanah_front', 'luas_bangunan_front', 'link', 'fasilitas', 'last_update','kamar_tidur', 'kamar_mandi', 'luas_tanah', 'luas_bangunan', 'carport', 'tipe_properti', 'sertifikat', 'daya_listrik', 'kamar_pembantu', 'kamar_mandi_pembantu', 'dapur', 'ruang_makan', 'ruang_tamu', 'kondisi_perabotan', 'material_bangunan', 'material_lantai', 'jumlah_lantai', 'hadap', 'konsep_dan_gaya_rumah', 'pemandangan', 'terjangkau_internet', 'lebar_jalan', 'tahun_dibangun', 'tahun_di_renovasi', 'sumber_air', 'hook', 'kondisi_properti', 'tipe_iklan', 'id_iklan', 'deskripsi', 'garasi', 'nomor_lantai']

    for col in desired_columns:
        if col not in df.columns:
            df[col] = None

    # Urutkan kolom sesuai daftar kolom yang diinginkan
    df = df[desired_columns]

    df = df[~df['link'].isin(scraped_link)]

    return df, len(df)

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def main(connection, log, engine, scraped,scraped_link):
    start = time.time()
    log_handler(connection, log, 'Delete Scraped Data...')
    connection.execute(scraped.delete())

    log_handler(connection, log, 'Get Rumah123 Data...')
    df_cover = get_first_data(driver, 1, connection, log)

    log_handler(connection, log, 'Get All Data...')
    save_list = get_all_data(df_cover, driver, connection, log)

    # Preprocess
    log_handler(connection, log, 'First Preprocess Data...')
    df_detail = pd.DataFrame(save_list)
    df_full = pd.merge(df_cover, df_detail, "left", on = "link").drop_duplicates(subset='link')
    df_full, jumlah = miss_handler_n_filter(df_full, scraped_link)

    # Export
    if jumlah == 0:
        log_handler(connection, log, 'Data is Up To Date!')
    else:
        log_handler(connection, log, 'Exporting Data...')
        # df_full.to_csv('users_properti.csv', index=False)
        df_full.to_sql('users_properti', con=engine, index=False, if_exists='append')

    stop = time.time()
    waktu = stop-start
    log_handler(connection, log, f'Scrap Complete on: {waktu}')


if __name__ == "__main__":
    main()
    

