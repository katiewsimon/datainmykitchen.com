from flask import Flask, Response, render_template, request
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps, loads
import re

app = Flask('datainmykitchen')
mongo = PyMongo(app)

@app.route('/search')
def food_search_view():
    return render_template('food_search.html')

@app.route('/food_types/search')
def get_all_food_types():
  q = request.args.get('q')
  print('q is')
  print(q)
  if q is None:
    response_json = "{}"
  else:
    regx = re.compile(q, re.IGNORECASE)
    results = mongo.db.food_data.find({"Shrt_Desc": regx})
    results_json = loads(dumps(results))

    print("results json")
    print(results_json)

    if len(results_json) > 0:
      foods = []
      for result_json in results_json:
        foods.append({'label': result_json.get('Shrt_Desc')})

      response_json = dumps(foods)
    else:
      response_json = "{}"

  resp = Response(response_json, status=200, mimetype='application/json')
  return resp

if __name__ == '__main__':
    app.run(debug=True)
