import pandas as pd
import pickle
from model.preprocessing import Preprocessing, COLS_TO_DELETE, COLS_TO_SCALE

EXPECTED_COLUMNS = [
    'popularity', 'danceability', 'energy', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'duration',
    'loudness_scale', 'tempo_scale'
]


class AppPreprocessing(Preprocessing):
    def transform_request_to_df(self, request):
        data = request.get_json()['data']
        df = pd.DataFrame([data])
        df = self.delete_columns(df, columns=COLS_TO_DELETE)
        df = self.scale(df, COLS_TO_SCALE)
        df = self.format(df)
        df = self.check_and_reorder_columns(df)
        return df

    def scale(self, df, cols=[]):
        for col in cols:
            if col in df.columns:
                with open(f'model/scalers/{col}.pkl', 'rb') as scaler_file:
                    scaler = pickle.load(scaler_file)
                df.loc[:, f'{col}_scale'] = scaler.transform(df[[col]])
                df = self.delete_columns(df, [col])
        return df

    def check_and_reorder_columns(self, df):
        if not all(col in df.columns for col in EXPECTED_COLUMNS):
            raise ValueError(
                "The DataFrame got by the Json Request does not "
                "contain all the required columns."
            )
        return df[EXPECTED_COLUMNS]
