from flask import abort, request, jsonify, Flask
import bs4
app = Flask(__name__) 
import requests

@app.route("/livecount", methods = ["POST", "GET"])
def livecount():
    req = request.get_json()
    print(f"[REQ], {req}")

    country = req["queryResult"]["parameters"]["country"]

    try:
        
        res = requests.get(f'https://api.covid19api.com/live/country/{country}/status/deaths').json()
        print(f"[RES] {res[-1]}")
        
        active = res[-1]["Active"]
        
        message = f"They are {active} active cases in {country}" 
        response = {
            "fulfillmentText": message,
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [ message ]
                    }
                }
            ]
        }
        
        return response
    except Exception as e:
        print(f"[ERROR] {e}")
        abort(500, str(e))
    

if __name__ == "__main__":
    app.run(debug = True)
