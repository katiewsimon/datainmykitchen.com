from flask import Flask, Response, render_template
import json
app = Flask(__name__)

@app.route("/search")
def food_search_view():
    return render_template("food_search.html")

@app.route("/food_types/all")
def get_all_food_types():
    js = json.dumps({"food_types": [
        {
            "name": "butter",
            "id": 1
        },
        {
            "name": "cheese",
            "id": 2
        },
        {
            "name": "bread",
            "id": 3
        },
        {
            "name": "clam chowder",
            "id": 4
        }
    ]})

    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(debug=True)
