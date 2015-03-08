from flask import Flask, Response, render_template, request
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps, loads
import re

app = Flask('datainmykitchen')
mongo = PyMongo(app)

@app.route('/recommendation')
def get_recommendation_for_foods():
    food_ids = request.args.get('foods').split(',')
    food_ids = map(int, food_ids)
    foods = mongo.db.food_data.find({"NDB_No": {'$in': food_ids}})

    response = {}

    for food in foods:
       response[food.get('Shrt_Desc')] = 'ok'

    response['boom'] = 5

    response_json = dumps({"example" : response})
    resp = Response(response_json, status=200, mimetype='application/json')
    return resp

@app.route('/search')
def food_search_view():
    return render_template('food_search.html')

@app.route('/food_types/search')
def get_all_food_types():
    q = request.args.get('q')

    if q is None:
        response_json = "{}"
    else:
        regx = re.compile(q, re.IGNORECASE)
        results = mongo.db.food_data.find({"Shrt_Desc": regx})
        results_json = loads(dumps(results))

    if len(results_json) > 0:
        foods = []
        for result_json in results_json:
            foods.append(
                {
                    'label': result_json.get('Shrt_Desc'),
                    'value': result_json.get('Shrt_Desc'),
                    'NDB_No': result_json.get('NDB_No')
                }
            )

        response_json = dumps(foods)
    else:
        response_json = "{}"

    resp = Response(response_json, status=200, mimetype='application/json')

    return resp

if __name__ == '__main__':
    app.run(debug=True)
