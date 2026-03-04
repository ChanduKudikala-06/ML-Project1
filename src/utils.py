#Common functions

import os
import sys
import dill

from src.exception import CustomException

from sklearn.metrics import r2_score

def save_object(file_path,obj):

    try:
        dir_path=os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:#This pickel file is saved in filepath
            dill.dump(obj,file_obj)#dill is used for pickle file

    except Exception as e:
        raise CustomException(e,sys)


def evaluate_model(X_train,y_train,X_test,y_test,models):

    try:
        report={}

        for i in range(len(list(models))):

            model=list(models.values())[i]#Accessing models
            model.fit(X_train,y_train) #Train Model

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            
            #model.keys()->contain all keys like LinearRegrssion,Decision Tree
            #[] represents indexing of i to store keys
            report[list(models.keys())[i]]=test_model_score
            #report["LinearRegression"]=0.82 it will trat like this

        return report
    
    
    
    except Exception as e:
        raise CustomException(e,sys)