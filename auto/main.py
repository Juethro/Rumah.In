from sqlalchemy import create_engine, MetaData, Table, Select
from script import rumah123_scrap
from script import prepo

engine = create_engine('mysql+pymysql://root:my-secret-pw@127.0.0.1:3306/django_tester')
connection = engine.connect()
metadata = MetaData()

# Preparation
log = Table('users_autolog', metadata, autoload_with=engine) # autolog table
train = Table('users_training', metadata, autoload_with=engine) # train table

scraped_link = [row[0] for row in connection.execute(Select(train.c.link)).fetchall()] # Filter duplicate Data with train table

def run_main():
    # Scraping
    rumah123_scrap.main(connection, log, engine, scraped_link)

    # Preprocessing (Belum Selesai)
    # prepo.main(connection, log, engine)
    
    connection.close()

if __name__ == "__main__":
    run_main()
