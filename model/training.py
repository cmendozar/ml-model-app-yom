# THIS FILE IS A SCHEMA TO WORK WITH DS TRANINNG MODEL PROCESSES AND DS LOGICS.
# LIKE IS A ML ENGINEER CHALLENGE IS NOT THE SCOPE TO GET OPTIMIZED MODEL ITS FOR DS.
# THIS FILE SHOUD BE USED FOR DATASCIENTIS TO MODEL TRANING LOGIC.
# I WILL SET A STANDARD METHOD I CONSIDER HAS TO BE HERE HAHAH.
# I WILL SAVE THE BEST MODEL USED IN JUPYTER SPIKE CHALLENGE NOTBOOK HERE.
# HERE ALSO I GET THE MODEL FROM ENTREGABLE 5 OF SPIKE CHALLENGE.

import pickle
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import GradientBoostingClassifier


class Training:
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def balance_data(self):
        sm = SMOTE(random_state=0)
        self.X_res, self.y_res = sm.fit_resample(self.X, self.y)
        return self.X_res, self.y_res

    def traning_model(self):
        classifer_GB = GradientBoostingClassifier(
            random_state=0,
            subsample=0.8,
            n_estimators=300,
            # presort=True,
            warm_start=True,
            max_features=None,
            min_samples_split=106,
            min_samples_leaf=177,
        )
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
