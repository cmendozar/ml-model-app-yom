import os
import pandas as pd

from preprocessing import Preprocessing
from training import Training


class ModelPipeline(Preprocessing, Training):
    def __init__(self, df1, df0, dft):
        self.df1 = df1
        self.df0 = df0
        self.dft = dft

    def run(self):
        prepro_step = Preprocessing(self.df1, self.df0, self.dft)
        self.X, self.y = prepro_step.run()
        train_step = Training(self.X, self.y)
        train_step.run()
        self.model = train_step.model


if __name__ == '__main__':
    data_path = 'data/t1/'
    print(os.getcwd())
    df_class1 = pd.read_csv(data_path + 'data_reggaeton.csv', sep=',')
    df_class0 = pd.read_csv(data_path + 'data_todotipo.csv', sep=',')
    df_test = pd.read_csv(data_path + 'data_test.csv')
    pipeline = ModelPipeline(df_class1, df_class0, df_test)
    pipeline.run()
    print(pipeline.model.predict(pipeline.X))
