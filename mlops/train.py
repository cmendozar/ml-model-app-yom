import os
import pandas as pd
import numpy as np

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sklearn.ensemble import GradientBoostingClassifier

import neptune
import neptune.integrations.sklearn as npt_utils

from model.training import Training
from model.preprocessing import Preprocessing


PARAMETERS = {
    "random_state": 0,
    "subsample": 0.8,
    "n_estimators": 300,
    "warm_start": True,
    "max_features": None,
    "min_samples_split": 106,
    "min_samples_leaf": 177,
}


class NeptuneTrain(Training):
    def __init__(self, X, y):
        super().__init__(X, y)
        self.project = os.environ.get("NEPTUNE_PROJECT")
        self.api_token = os.environ.get("NEPTUNE_API_TOKEN")
        if not self.project or not self.api_token:
            raise ValueError(
                "Enviroments variable not setted correctly"
            )
        self.run = None

    def start_run(self):
        self.run = neptune.init_run(
            project=self.project,
            api_token=self.api_token
        )
        return self.run

    def set_parameters(self):
        super().set_parameters(PARAMETERS)
        self.run["parameters"] = self.parameters

    def run_training(self):
        self.start_run()
        self.set_parameters()
        self.balance_data()
        self.traning_model()
        self.set_neptune_info()

    def traning_model(self):
        gbc = GradientBoostingClassifier(**self.parameters)
        gbc.fit(self.X_train, self.y_train)
        self.gbc = gbc

    def set_neptune_info(self):
        self.run["classifier"] = npt_utils.create_classifier_summary(
            self.gbc, self.X_train, self.X_test, self.y_train, self.y_test
        )
        self.run["cls_summary"] = npt_utils.create_classifier_summary(
            self.gbc, self.X_train, self.X_test, self.y_train, self.y_test
        )
        self.run["confusion-matrix"] = npt_utils.create_confusion_matrix_chart(
            self.gbc, self.X_train, self.X_test, self.y_train, self.y_test
        )

    def stop(self):
        if self.run:
            self.run.stop()


if __name__ == '__main__':
    data_path = 'data/t1/'
    df_class1 = pd.read_csv(data_path + 'data_reggaeton.csv', sep=',')
    df_class0 = pd.read_csv(data_path + 'data_todotipo.csv', sep=',')
    preprocessing = Preprocessing(
        df_class1=df_class1,
        df_class0=df_class0,
        df_test=None
    )
    X, y = preprocessing.run()
    nt = NeptuneTrain(X, y)
    nt.run_training()
    nt.stop()
