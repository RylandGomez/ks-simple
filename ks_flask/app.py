import pickle
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
from flask import Flask, request, render_template
from .preprocessing import get_dur, get_monthyear, predict_to_string

def create_app():
    '''
    Instantiation and definition of Flask app and routes.
    '''
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    
    def main():
        '''
        Landing page that renders data submission.
        '''
        return render_template("submit_data.html")



    @app.route("/predict", methods=["GET", "POST"])
    def predict():
        '''
        App route for receiving front end predictive data and
        generating a prediction. Returns prediction as a string
        response.
        '''
        if request.method == 'POST':
            data = request.form.to_dict()

            # Run feature engineering functions
            data['duration'] = get_dur(data['date'], data['deadline'])
            data['month'], data['year'] = get_monthyear(data['date'])

            # Define desired variables in X_pred order
            X_vars = ['goal','month','year','duration','country','currency','category']

            # Create empty list for populating X_pred
            X_pred_list = []

            # Iterate over X_vars to populate X_pred with key value pairs
            for x in X_vars:
                X_pred_list.append(data[x])

            # Format list into 2D array for prediction
            X_pred = np.array(X_pred_list)
            X_pred = X_pred.reshape(1,-1)

            # Load locally stored pickled model
            model = pickle.load(open('ks_flask/model','rb'))
            
            # Create prediction from model
            prediction = model.predict(X_pred)

            # Covert array to string response
            results = predict_to_string(prediction)

        else:
            results = 'No data has been posted to page.'
        
        return render_template("results.html", results=results)
        

    return app