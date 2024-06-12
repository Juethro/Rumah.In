from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sqlalchemy import create_engine, Table, insert, MetaData
import datetime
import pandas as pd
import pickle

def log_handler(connection, log, msg):
    instruction = insert(log).values(log=f'{msg}', date=datetime.datetime.now())
    connection.execute(instruction)
    connection.commit()

def model_input(connection, model_regression, path):
    instruction = insert(model_regression).values(waktu=datetime.datetime.now(), versi='v1', path=path)
    connection.execute(instruction)
    connection.commit()

def main():
    engine = create_engine('mysql+pymysql://root:my-secret-pw@127.0.0.1:3306/django_tester')
    conn = engine.connect()
    metadata = MetaData()
    log = Table('users_autolog', metadata, autoload_with=engine) # autolog table
    modelregresi = Table('users_modelregresi', metadata, autoload_with=engine) # modelregresi table

    log_handler(conn, log, "Model Fetching Data...")
    try:
        df = pd.read_sql('users_training', con=engine)
        df = df.drop(columns=['id','judul', 'link', 'images_link','kecamatan_1'])
        X = df.drop(columns=['harga'])
        y = df.harga
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    except Exception as e:
        log_handler(conn, log, "Model Fetching Failed!")

    log_handler(conn, log, "Model Modeling...")
    try:
        model = XGBRegressor()
        # Tentukan grid parameter yang ingin Anda jelajahi
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [3, 4, 5, 6, 7, 8, 9, 10],
            'learning_rate': [0.01, 0.1, 0.3],
            'gamma': [0, 0.1, 0.2],
            'random_state': [42]
        }
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='r2', verbose=0, n_jobs=-1)
        grid_search.fit(X, y)
        
        
    except Exception as e:
        log_handler(conn, log, "Model Modeling Failed!")
    
    log_handler(conn, log, "Model Export...")
    try:
        current_time = datetime.datetime.now()
        filename = f"model_{current_time}.pickle"
        model_input(conn, modelregresi, f'/web/auto/models/{filename}')
        with open(f'./auto/models/{filename}', 'wb') as f:
            pickle.dump(grid_search, f)
    except Exception as e:
        log_handler(conn, log, "Model Export Failed!")

if __name__ == "__main__":
    main()
