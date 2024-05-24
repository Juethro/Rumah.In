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
        "luas tanah" : [],
        "luas bangunan" : [],
        "link" : []
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
        section_class = soup.find_all(class_="card-featured__middle-section")
        for section in section_class:
            data["judul"].append(section.find("h2").get_text())
            data["harga"].append(section.find("strong").get_text())
            data["cicilan"].append(section.find("em").get_text())
            data["kecamatan"].append([kecamatan.get_text() for kecamatan in section.find_all("span") if "Surabaya" in kecamatan.get_text()][0])
            data["luas tanah"].append(section.find_all(class_ = "attribute-info")[0].get_text().replace("LT : ", ""))
            try:
                data["luas bangunan"].append(section.find_all(class_ = "attribute-info")[1].get_text().replace("LB : ", ""))
            except:
                data["luas bangunan"].append("")
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
                data_full[item.get_text()] = value.get_text()
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

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def main(connection, log, engine):
    start = time.time()
    log_handler(connection, log, 'Get Rumah123 Data...')
    df_cover = get_first_data(driver, 3, connection, log)

    log_handler(connection, log, 'Get All Data...')
    save_list = get_all_data(df_cover, driver, connection, log)

    log_handler(connection, log, 'Exporting Data...')
    df_detail = pd.DataFrame(save_list)
    df_full = pd.merge(df_cover, df_detail, "left", on = "link")
    df_full.to_sql('users_properti', con=engine, if_exists='replace', index=False)

    stop = time.time()
    waktu = stop-start
    log_handler(connection, log, f'Scrap Complete on: {waktu}')


if __name__ == "__main__":
    main()
    

