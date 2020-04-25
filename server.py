from flask import abort, request, jsonify, Flask, render_template
import requests
import os
from json import dumps

app = Flask(__name__, template_folder=os.path.abspath("./static"))

@app.route("/")
def frontend():
    return render_template("index.html")

@app.route("/chatbot", methods = ["POST", "GET"])
def receive():
    req = request.get_json()
    print(f"[REQ], {dumps(req, indent=2)}")
    intentName= req["queryResult"]["intent"]["displayName"]
    if intentName == "liveCases":
        country = req["queryResult"]["parameters"]["country"]  
        return livecount(country)
    # elif intentName[0] == "Q":
    return {}


def livecount(country):
    try:
        print(country)
        res = requests.get(f'https://api.covid19api.com/live/country/{country}/status/deaths').json()[-1]
        print(f"[RES] {res}")
        
        active = res["Active"]
        confirmed = res["Confirmed"]
        recovered = res["Recovered"]
        deaths = res["Deaths"]
        date = res["Date"][:10]
        formattedCountry = res["Country"]
        
        message = [
            f"In {formattedCountry}, there are:",
            f" - {active} active cases,",
            f" - {confirmed} confirmed cases,"
            f" - {recovered} recovered patients,",
            f" - {deaths} deaths.",
            "",
            f"This data is as of {date}"
        ]
        response = {
            "fulfillmentText": "\n".join(message),
            "fulfillmentMessages": [
                {      
                    "text": {
                        "text": message
                    }
                }
            ]
        }
        
        return response
    except Exception as e:
        print(f"[ERROR] {e}")
        abort(500, str(e))
    

if __name__ == "__main__":
    app.run(debug=True)
