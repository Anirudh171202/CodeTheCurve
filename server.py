from flask import abort, request, jsonify, Flask

app = Flask(__name__) 
import requests

@app.route("/livecount", methods = ["POST", "GET"])
def receive():
    req = request.get_json()
    print(f"[REQ], {req}")
    intentName= req["queryResult"]["intent"]
    if intentName == "liveCount":
        country = req["queryResult"]["parameters"]["country"]  
        return livecount(country)
    # elif intentName[0] == "Q":


        



def livecount(country):
    try:
        
        res = requests.get(f'https://api.covid19api.com/live/country/{country}/status/deaths').json()[-1]
        print(f"[RES] {res}")
        
        active = res["Active"]
        confirmed = res["Confirmed"]
        recovered = res["Recovered"]
        deaths = res["Deaths"]
        date = res["Date"][:10]
        
        message = f'''As of {date},
 there are {active} active cases, 
 {confirmed} confirmed cases, 
 {recovered} recovered patients, 
 {deaths} deaths'''
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
