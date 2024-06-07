# THIS FILE IS A SCHEMA TO WORK WITH DS TRANINNG MODEL PROCESSES AND DS LOGICS.
# LIKE IS A ML ENGINEER CHALLENGE IS NOT THE SCOPE TO GET OPTIMIZED MODEL ITS FOR DS.
# THIS FILE SHOUD BE USED FOR DATASCIENTIS TO MODEL TRANING LOGIC.
# I WILL SET A STANDARD METHOD I CONSIDER HAS TO BE HERE HAHAH.
# I WILL SAVE THE BEST MODEL USED IN JUPYTER SPIKE CHALLENGE NOTBOOK HERE.
# HERE ALSO I GET THE MODEL FROM ENTREGABLE 5 OF SPIKE CHALLENGE.

import pickle
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

PARAMETERS = {
    "random_state": 0,
    "subsample": 0.8,
    "n_estimators": 300,
    # presort: True,
    "warm_start": True,
    "max_features": None,
    "min_samples_split": 106,
    "min_samples_leaf": 177,
}


class Training:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = \
            train_test_split(self.X, self.y, random_state=0, test_size=0.3)

    def balance_data(self):
        sm = SMOTE(random_state=0)
        self.split_data()
        self.X_res, self.y_res = sm.fit_resample(self.X_train, self.y_train)
        return self.X_res, self.y_res

    def set_parameters(self, parameters):
        self.parameters = parameters

    def traning_model(self):
        self.set_parameters(PARAMETERS)
        classifer_GB = GradientBoostingClassifier(**self.parameters)
        self.balance_data()
        self.model = classifer_GB.fit(self.X_res, self.y_res)
        return self.model

    def optimize_model(self):
        # TODO: MAKE CODE FOR OPTIMIZE MODEL AND CHOOSE BETTER MODEL ETC.
        optimized_model = self.traning_model()
        return optimized_model

    def save_model(self, model, filename='model.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(model, file)
            print(f'Model has been saved as {filename}')

    def run(self):
        """
        Here the Pipeline to traning models.
        """
        self.traning_model()
        self.optimize_model()
        self.save_model(self.model)
