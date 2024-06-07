import os
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import MinMaxScaler


COLS_TO_DELETE = [
    'key',
    'mode',
    'id_new',
    'Unnamed: 0',
    'time_signature',
]

COLS_TO_SCALE = [
    'loudness',
    'tempo',
]


class Preprocessing():
    def __init__(self, df_class1, df_class0, df_test):
        self.df1 = df_class1
        self.df0 = df_class0
        self.dft = df_test

    def add_class_column(self):
        """
        Set the class 1 and class 0 columns for each DataFrame.
        Return:
         (1) DF Class 0
         (2) DF Class 1
        """
        self.df0['class'] = 1
        self.df1['class'] = 0

        # Dropna cases
        self.df0 = self.df0.dropna(how='any', axis=0).copy()
        self.df1 = self.df1.dropna(how='any', axis=0).copy()

        return self.df0, self.df1

    def merge_dfs(self):
        return pd.concat([self.df0, self.df1]).copy()

    def delete_columns(self, df, columns=[]):
        return df.drop(columns=[col for col in columns if col in df.columns])

    def format(self, df_train):
        df = df_train.copy()
        df_columns = df.columns
        if 'popularity' in df_columns:
            df['popularity'] = df.popularity.astype('float64')
        if 'duration' in df_columns:
            df['duration'] = df.duration.astype('float64')
        if 'key' in df_columns:
            df["key_code"] = df.key.astype('category')
        if 'mode' in df_columns:
            df["mode_code"] = df['mode'].astype('category')
        if 'class' in df_columns:
            df['class'] = df['class'].astype('category')
        return df

    def scale(self, df, cols=[]):
        for col in cols:
            if col in df.columns:
                scaler = MinMaxScaler()
                df.loc[:, f'{col}_scale'] = scaler.fit_transform(df[[col]])
                df = self.delete_columns(df, [col])
                with open(f'model/scalers/{col}.pkl', 'wb') as scaler_file:
                    pickle.dump(scaler, scaler_file)
        return df

    def make_feat_label_data(self, df):
        X = df.loc[:, df.columns != 'class']
        y = df['class'].to_numpy()
        return X, y

    def make_testing_data(self, df):
        df = self.dft
        return df

    def clean_dataset(self, df):
        "Method to deleted nan values"
        assert isinstance(df, pd.DataFrame)
        df.dropna(inplace=True)
        indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
        return df[indices_to_keep].astype(np.float64)

    def run(self):
        """
        Here the Pipeline to process and transform data to training models
        Return: X, y datasets for tranining model
        """
        self.add_class_column()
        df_train = self.merge_dfs()
        df_train = self.delete_columns(df_train, columns=COLS_TO_DELETE)
        df_train = self.clean_dataset(df_train)
        df_train = self.scale(df_train, COLS_TO_SCALE)
        df_train = self.format(df_train)
        X, y = self.make_feat_label_data(df_train)
        return X, y


if __name__ == '__main__':
    data_path = 'data/t1/'
    print(os.getcwd())
    df_class1 = pd.read_csv(data_path + 'data_reggaeton.csv', sep=',')
    df_class0 = pd.read_csv(data_path + 'data_todotipo.csv', sep=',')
    df_test = pd.read_csv(data_path + 'data_test.csv')
    prepross = Preprocessing(df_class0, df_class1, df_test)
    X, y = prepross.run()
    print(X.head(), y[:5])
