
# https://docs.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-direct-line-3-0-authentication?view=azure-bot-service-4.0
import requests
from os import environ
from flask import Flask
from flask_cors import CORS

# Get environment variables
PORT = int(environ.get("PORT", 3000))
SECRET_KEY = environ.get("MS_KEY_SECRET", "")

api = Flask(__name__)
CORS(api)  # Allow request from any origin


@api.route("/token")
def token():

    url = 'https://directline.botframework.com/v3/directline/tokens/generate'
    header = {'Authorization': f'Bearer {SECRET_KEY}'}

    # Send a request to Azure
    response = requests.post(url, headers=header)

    # Return the token
    if response.status_code == 200:
        return {"token": response.json()['token'], 'status': True}

    # Return a status False if no token was received
    return {"token": None, "status": False}


# Run the app
if __name__ == '__main__':
    api.run('0.0.0.0', port=PORT, debug=False, threaded=True)
