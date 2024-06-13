from sqlalchemy import create_engine, MetaData, Table, Select, insert
from script import rumah123_scrap
from script import prepo
import datetime

engine = create_engine("mysql+pymysql://root:my-secret-pw@127.0.0.1:3306/django_tester")
connection = engine.connect()
metadata = MetaData()

# Preparation
log = Table('users_autolog', metadata, autoload_with=engine) # autolog table
train = Table('users_training', metadata, autoload_with=engine) # train table
scraped = Table('users_properti', metadata, autoload_with=engine) # scraped table

scraped_link = [row[0] for row in connection.execute(Select(train.c.link)).fetchall()] # Filter duplicate Data with train table

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def main():
    # Scraping
    log_handler(connection, log, "Scraping Start...")
    try:
        rumah123_scrap.main(connection, log, engine, scraped,scraped_link)
    except Exception as e:
        log_handler(connection, log, "Scraping Failed!")

    # Preprocessing (Belum Selesai)
    log_handler(connection, log, "Preprocessing Start...")
    # try:
    prepo.main(connection, log, engine)
    # except Exception as e:
    #     log_handler(connection, log, "Preprocessing Failed!")
    
    connection.close()

if __name__ == "__main__":
    main()
