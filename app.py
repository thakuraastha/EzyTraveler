import os
import requests
from flask import Flask, render_template, request
import mapbox

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Replace this with your own Mapbox API access token
MAPBOX_ACCESS_TOKEN = 'your_mapbox_access_token'

geocoder = mapbox.Geocoder(access_token=MAPBOX_ACCESS_TOKEN)

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    response = geocoder.forward(query)
    location_data = response.geojson()['features'][0]

    coords = location_data['geometry']['coordinates']
    place_name = location_data['place_name']

    wikipedia_params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'utf8': 1,
        'formatversion': 2
    }

    wikipedia_response = requests.get(WIKIPEDIA_API_URL, params=wikipedia_params).json()
    wikipedia_page_id = wikipedia_response['query']['search'][0]['pageid']

    wikipedia_params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'pageids': wikipedia_page_id,
        'explaintext': 1,
        'utf8': 1,
        'formatversion': 2
    }

    wikipedia_response = requests.get(WIKIPEDIA_API_URL, params=wikipedia_params).json()
    wikipedia_extract = wikipedia_response['query']['pages'][0]['extract']

    return render_template('result.html', coords=coords, place_name=place_name, wikipedia_extract=wikipedia_extract)

if __name__ == '__main__':
    app.run(debug=True)
