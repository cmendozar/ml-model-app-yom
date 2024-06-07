import pickle
import pandas as pd
from datetime import datetime
from utils.mongo_handler import MongoHandler
from app.preprocessing import AppPreprocessing


if __name__ == '__main__':
    data_path = 'data/t1/'
    df_class1 = pd.read_csv(data_path + 'data_reggaeton.csv', sep=',')
    df_class0 = pd.read_csv(data_path + 'data_todotipo.csv', sep=',')
    df_test = pd.read_csv(data_path + 'data_test.csv')
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    preprocessor = AppPreprocessing(None, None, None)
    data_test = preprocessor.transform_test_df(df_test)
    data_test['prediction'] = model.predict(data_test)
    data_test['timestamp'] = datetime.now()
    handler = MongoHandler("URI_YOM_MONGO", "yom", "ml-app")
    handler.insert_df_to_col(data_test)
