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
        
        res = requests.get(f'https://api.covid19api.com/live/country/{country}/status/deaths')
        print(f"[RES] {res.json()[-1]}")
        response = {
            "fulfillmentMessages": [
                {
                "text": {
                    "cases": res.json()[-1]
                }
                }
            ]
            }
        return res.json()[-1]
    except Exception as e:
        print(f"[ERROR] {e}")
        abort(500, str(e))
    

if __name__ == "__main__":
    app.run(debug = True)
