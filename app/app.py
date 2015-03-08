from flask import Flask, Response, render_template, request
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps, loads
import re, operator

app = Flask('datainmykitchen')
mongo = PyMongo(app)

@app.route('/recommendation')
def get_recommendation_for_foods():
    food_ids = request.args.get('foods').split(',')
    food_ids = map(int, food_ids)
    foods = mongo.db.food_data.find({"NDB_No": {'$in': food_ids}})
    nutrients = list(mongo.db.nutrients.find({}))

    # foods is the foods that the user inputs
    # loop through each food to grab the nutrient amount per nutrient category
    # sum the nutrient amount in each nutrient category for all the foods
    # append the nutrient amounts to the response

    nutrients_running_totals = {}

    counter = 0
    for food in foods:
        food_id = food.get('NDB_No')
        food_name = food.get('Shrt_Desc')
        print(food_name)

        for nutrient in nutrients:
            nutrient_name = nutrient.get('Nutrient')
            food_nutrient_val = food.get(nutrient_name)

            if not food_nutrient_val:
                food_nutrient_val = 0.0

            if not nutrient_name in nutrients_running_totals:
                nutrients_running_totals[nutrient_name] = food_nutrient_val
            else:
                nutrient_consumed = nutrients_running_totals[nutrient_name]
                nutrients_running_totals[nutrient_name] = nutrient_consumed + food_nutrient_val


    daily_values = {}
    percent_daily_values = []
    for nutrient in nutrients:
        name = nutrient.get('Nutrient')
        daily_value = nutrient.get('Daily Value')

        daily_values[name] = daily_value

        pdv = {}
        pdv['name'] = name
        pdv['value'] = nutrients_running_totals.get(name) / daily_value
        percent_daily_values.append(pdv)

    sorted_pdvs = sorted(percent_daily_values, key=lambda pdv: pdv['value'])

    response_json = dumps({"nutrients" : sorted_pdvs})
    resp = Response(response_json, status=200, mimetype='application/json')
    return resp

@app.route('/')
def food_search_view():
    return app.send_static_file('index.html')
    #return render_template('index.html')

@app.route('/food_types/search')
def get_all_food_types():
    q = request.args.get('q')

    if q is None:
        response_json = "{}"
    else:
        #regx = re.compile(q, re.IGNORECASE)
        #results = mongo.db.food_data.find({"Shrt_Desc": regx})
        text_results = mongo.db.food_data.find({'$text': {'$search': q }})
        print(text_results)
        results_json = loads(dumps(text_results))

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
