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
    nutrients = list(mongo.db.nutrients.find({}))
    # print(nutrients)


    response = []

    # foods is the foods that the user inputs
    # loop through each food to grab the nutrient amount per nutrient category
    # sum the nutrient amount in each nutrient category for all the foods
    # append the nutrient amounts to the response

    nutrients_consumed = {
    }
    counter = 0
    for food in foods:
        nutrient_amounts = {}
        food_id = food.get('NDB_No')
        food_name = food.get('Shrt_Desc')

        # print(nutrients)

        for nutrient in nutrients:
            nutrient_name = nutrient.get('Nutrient')
            food_nutrient_val = food.get(nutrient_name)
            # print(food_name + " : " + nutrient.get('Nutrient') + ' => ' )
            # print(food.get(nutrient_name))
            # 'fat' : 'Fat_(mg)'
            if not nutrient_name in nutrients_consumed:
                nutrients_consumed[nutrient_name] = food.get(nutrient_name)
            else:
                nut_consumed = nutrients_consumed[nutrient_name]
                food_nut_val = food.get(nutrient_name)
                # print(food_nut_val)
                # print(nut_consumed)
                # print("consumed: ")
                # print(int(nut_consumed))
                if nut_consumed is float:
                    print "nut_consumed is float"
                # (nut_consumed is float or nut_consumed is int or nut_consumed is None) and (food_nut_val is float or food_nut_val is int or food_nut_val is None):
                    # print(food_nut_val)
                    # print(nut_consumed)
                    nutrients_consumed[nutrient_name] = nut_consumed + food_nut_val
                else:
                    # print "not a float"
                    counter = counter + 1
        print(counter)
        response.append(nutrient_amounts)



    #response = [
    #        {
    #            'nutrient': 'Fat',
    #            'unique_id': 4124,
    #            'quantity': 0.8
    #        }
    #]
    #     nutrients_consumed = {
    # #     'fat': 0.6,
    # #     'sodium': 0.8
    # }

    response_json = dumps({"nutrients" : response})
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
