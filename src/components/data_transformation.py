import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object
@dataclass
class DataTransformationConfig:
    #For Deployment Purpose we use pickel file->artifacts/preprocessor.pkl
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    
    def get_data_transformer_object(self):

        '''
        This function is responsible is datatransformation
        '''

        try:
            
            numerical_features=['reading_score', 'writing_score']
            categorical_features=['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),#Handle Missing values
                    ("one_hot_encoding",OneHotEncoder()),#Converts text to numerical values
                    ("scaler",StandardScaler(with_mean=False))#It scales data
                ]
            )
            logging.info(f"numerical columns {numerical_features}")
            logging.info(f"categorical columns {categorical_features}")

            #Column transformer is used to apply different transformations to different columnnsin your dataset

            preprocessor=ColumnTransformer(
                [
                    ("num_pipelines",num_pipeline,numerical_features),
                    ("cat_pipelines",cat_pipeline,categorical_features)
                ]
            )

            return preprocessor

  
        except Exception as e:
            raise CustomException(e,sys)
        
    
    def initiate_data_transformation(self,train_path,test_path):

        try:
        
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining Preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns=['reading_score', 'writing_score']
            
            #dropping target columnn
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]


            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            
            #We are calling method that calls coulmn transformer object 
            #It goes to ColumnTransformer class and exceutes fit_transform method
            #Here transfoem is num_pipline and cat_pipeline
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)
            

            #np.c_ combine two arrays
            train_arr=np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)
            ]

            test_arr=np.c_[
                input_feature_test_arr,np.array(target_feature_test_df)
            ]

            logging.info("Saved Processing object")
            

            #It will call save_object from utils.py
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path

            )      
        
        except Exception as e:
            raise CustomException(e,sys)
            
            


