from sqlalchemy import create_engine, MetaData, Table
from script import rumah123_scrap

engine = create_engine('mysql+pymysql://root:@localhost:3306/django_tester')
connection = engine.connect()
metadata = MetaData()
log = Table('users_autolog', metadata, autoload_with=engine)

def run_main():
    rumah123_scrap.main(connection, log, engine)

if __name__ == "__main__":
    run_main()
