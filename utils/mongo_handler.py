import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime


class MongoHandler:
    def __init__(self, uri_env_var, db_name, col_name):
        self.uri = os.environ.get(uri_env_var)
        if not self.uri:
            raise ValueError(f"Environment variable '{uri_env_var}' not found")
        self.client = MongoClient(
            self.uri,
            server_api=ServerApi('1'),
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        self.db = self.client[db_name]
        self.col = self.db[col_name]
        self._check_connection()

    def _check_connection(self):
        try:
            self.client.admin.command('ping')
            print(
                "Pinged your deployment."
                "You successfully connected to MongoDB!"
            )
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def insert_df_to_col(self, df):
        records = df.to_dict(orient='records')
        try:
            insert_result = self.col.insert_many(records)
            print(f"Inserted IDs: {insert_result.inserted_ids}")
        except Exception as e:
            print(f"Error inserting records: {e}")

    def save_request_data(self, request_data, prediction):
        document = {
            'popularity': float(request_data['data'].get('popularity', 0)),
            'danceability': float(request_data['data'].get('danceability', 0)),
            'energy': float(request_data['data'].get('energy', 0)),
            'speechiness': float(request_data['data'].get('speechiness', 0)),
            'acousticness': float(request_data['data'].get('acousticness', 0)),
            'instrumentalness': float(
                request_data['data'].get('instrumentalness', 0)
            ),
            'liveness': float(request_data['data'].get('liveness', 0)),
            'valence': float(request_data['data'].get('valence', 0)),
            'duration': float(request_data['data'].get('duration', 0)),
            'loudness_scale': float(
                request_data['data'].get('loudness_scale', 0)
            ),
            'tempo_scale': float(request_data['data'].get('tempo_scale', 0)),
            'prediction': float(prediction[0]),
            'timestamp': datetime.now()
        }
        try:
            insert_result = self.col.insert_one(document)
            print(f"Inserted ID: {insert_result.inserted_id}")
        except Exception as e:
            print(f"Error inserting record: {e}")
