from flask import Flask,request,render_template

#request->Gets data from HTML form
#render_template->Sends HTML Page to browser

import numpy as np
import pandas as pd


from sklearn.preprocessing import StandardScaler

from src.pipeline.predict_pipeline import CustomData,PredictPipeline

#creates web server
application=Flask(__name__)


app=application#->Used for cloud platforms to deploy this project



#Route for Home Page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    #Get request happens when a user opens a page
    #Post request happens when form data is submitted
    #Loads HTML Form
    if request.method=='GET':
        return render_template('home.html')
    
    #Post Condition->When User submits the form
    #when user submits form dynamically url will generate by using this function so url will be /predictdata
    #<form action="{{ url_for('predict_datapoint')}}" method="post">
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))

        )

        pred_df=data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        
        #Flask sends data to template and jinja processes the template 
        #Jinja engine reads the HTML file and replaces variable using {{}} in html
        return render_template('home.html',results=results[0])
    

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080)
    #While deploting remove this debug=True
