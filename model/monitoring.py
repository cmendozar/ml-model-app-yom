# DUE WE DONT KNOW IF THE PREDICCITION ARE RIGHT
# WE WILL MONITORING DATA DERIVATE AND CONCEPT/MODEL DERIVATE

import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import ks_2samp

from model.preprocessing import Preprocessing
from utils.mongo_handler import MongoHandler
from mlops.monitoring import NepMonitoring

COLS_TO_COMPARE = [
    "popularity", "danceability", "energy", "key",
    "loudness", "mode", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence",
    "tempo", "duration"# , "class"
]


class Monitoring:
    def __init__(self, mongo_uri, mongo_db, mongo_collection, data_path):
        self.mongo_handler = MongoHandler(mongo_uri, mongo_db, mongo_collection)
        self.data_path = data_path

    def compare_distributions(self, df1, df2, columns):
        results = {}
        for col in columns:
            if col in df1.columns and col in df2.columns:
                k2, p_value = ks_2samp(df1[col], df2[col])
                results[col] = {
                    'k2': k2,
                    'p_value': p_value,
                    'df1_descriptive': self.get_descriptive_stats(df1[col]),
                    'df2_descriptive': self.get_descriptive_stats(df2[col])
                }
            else:
                results[col] = {
                    'k2': None,
                    'p_value': None,
                    'df1_descriptive': None if col not in df1.columns else self.get_descriptive_stats(df1[col]),
                    'df2_descriptive': None if col not in df2.columns else self.get_descriptive_stats(df2[col]),
                    'error': 'Column not found in one of the dataframes'
                }
        return results

    def get_descriptive_stats(self, series):
        return {
            'mean': series.mean(),
            'median': series.median(),
            'std': series.std(),
            'min': series.min(),
            'max': series.max(),
            '25%': series.quantile(0.25),
            '50%': series.quantile(0.5),
            '75%': series.quantile(0.75)
        }

    def get_mongo_data(self):
        date_threshold = datetime.now() - timedelta(weeks=1)
        query = {"timestamp": {"$gte": date_threshold}}
        mongo_data = list(self.mongo_handler.col.find(query))

        df_mongo = pd.DataFrame(mongo_data)
        for col in df_mongo.columns:
            if col in COLS_TO_COMPARE:
                df_mongo[col] = df_mongo[col].apply(
                    lambda x: float(x['$numberDouble']) if isinstance(x, dict) and '$numberDouble' in x else x
                )
        # df_mongo.rename(columns={'Prediction': 'class'}, inplace=True)
        return df_mongo

    def load_data(self):
        df_class1 = pd.read_csv(self.data_path + 'data_reggaeton.csv', sep=',')
        df_class0 = pd.read_csv(self.data_path + 'data_todotipo.csv', sep=',')
        df_test = pd.read_csv(self.data_path + 'data_test.csv')
        prepross = Preprocessing(df_class0, df_class1, df_test)
        df_train = prepross.merge_dfs()
        return df_train

    def run_monitoring(self):
        df_train = self.load_data()
        df_mongo = self.get_mongo_data()
        df_train = df_train.dropna(subset=COLS_TO_COMPARE)
        neptune_monitoring = NepMonitoring()
        neptune_monitoring.start_run()
        comparison_results = self.compare_distributions(df_train, df_mongo, COLS_TO_COMPARE)
        neptune_monitoring.log_results_to_neptune(comparison_results)  # Log results to Neptune
        neptune_monitoring.stop_run()
        print("Monitoring excuted")


if __name__ == '__main__':
    data_path = 'data/t1/'
    mongo_uri = 'URI_YOM_MONGO'
    mongo_db = 'yom'
    mongo_collection = 'ml-app'

    monitoring = Monitoring(mongo_uri, mongo_db, mongo_collection, data_path)

    df_train = monitoring.load_data()
    df_mongo = monitoring.get_mongo_data()

    # Drop the rows with missing values in df_train
    df_train = df_train.dropna(subset=COLS_TO_COMPARE)

    neptune_monitoring = NepMonitoring()  # Initialize Neptune monitoring
    neptune_monitoring.start_run()  # Start Neptune run

    comparison_results = monitoring.compare_distributions(df_train, df_mongo, COLS_TO_COMPARE)
    neptune_monitoring.log_results_to_neptune(comparison_results)  # Log results to Neptune

    neptune_monitoring.stop_run()  # Stop Neptune run

    print(comparison_results)
