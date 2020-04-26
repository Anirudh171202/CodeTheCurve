from flask import abort, request, jsonify, Flask, render_template
import requests
import os,sys
from json import dumps
from googletrans import Translator
import dialogflow_v2 as dialogflow
from uuid import uuid4
from dotenv import load_dotenv

session_id = str(uuid4)


def translate(text, lang="en"):
    trans = Translator()
    t = trans.translate(text, lang)
    res = t.text
    src = t.src
    return res, src    

app = Flask(__name__, template_folder=os.path.abspath("./static"))

@app.route("/")
def frontend():
    return render_template("index.html")

@app.route("/dialogflow-chatbot", methods=["POST", "GET"])
def dialogflow_request():
    req = request.get_json()
    print(f"[REQ], {dumps(req, indent=2)}")
    intentName= req["queryResult"]["intent"]["displayName"]
    # if intentName == "liveCases":
    country = req["queryResult"]["parameters"]["country"]  
    return livecount(country)
    # elif intentName[0] == "Q":
    # return {}

@app.route("/chatbot", methods=["POST", "GET"])
def chatbot():
    req = request.get_json()
    print(req)
    res, src = translate(req["text"])

    # TODO Dialogflow stuff
    dialogflowResponse = detect_intent_texts(res)

    text = translate(dialogflowResponse, src)[0]
    print(text)
    return {
        "text": text
    }

def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputsprint.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    # os.system('export GOOGLE_APPLICATION__CREDENTIALS="`pwd`/google_auth.json"')
    print(load_dotenv())
    print("[OS ENVIRON]", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
    project_id = os.environ["PROJECT_ID"]
    session_client = dialogflow.SessionsClient()
    language_code = "en"
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response.query_result.fulfillment_text

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
