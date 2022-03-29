#!/usr/bin/env python
'''
Implement the app interface

Author: ucaiado
Date: March 2022
'''
import json
import pathlib

from flask import Flask, jsonify, request

try:
    from . import diagnostics
    from .scoring import score_model
except ImportError:
    import diagnostics
    from scoring import score_model


# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'


path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


# Hello World Endpoint
@app.route("/", methods=['GET', 'OPTIONS'])
def hello_world():
    '''
    check the Hello World! of the deployed model
    '''
    return jsonify({'response': 'Hello world!!'})

# Prediction Endpoint


@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predicting():
    '''
    call the prediction function you created in Step 3 add return value for
     prediction outputs
    '''
    dataset_path = request.args.get('dataset_path')
    dataset_path = str(path_to_conf / pathlib.Path(dataset_path))
    y_preds = diagnostics.model_predictions(this_data=dataset_path)
    return jsonify({'predictions': [int(x) for x in y_preds]})


# Scoring Endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def score():
    '''
    check the score of the deployed model
    '''
    f_score = score_model()
    return jsonify({'model_score': f_score})


# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def summarizing():
    '''
    check means, medians, and modes for each column
    '''
    l_out = diagnostics.dataframe_summary(
        str(path_to_conf / 'ingesteddata' / 'finaldata.csv'))
    return jsonify({'summary': l_out})


# Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def diagnosing():
    '''
    check timing and percent NA values
    '''
    d_out = {}
    d_out['execution_time'] = diagnostics.execution_time()
    d_out['outdated_packages'] = diagnostics.outdated_packages_list()
    d_out['missing_values'] = diagnostics.count_missing_values()
    return jsonify(d_out)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
