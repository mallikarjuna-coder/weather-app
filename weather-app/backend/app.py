from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    api_key = os.getenv('API_KEY')

    if not city:
        return jsonify({'error': 'City is required'}), 400

    try:
        response = requests.get(
            'http://api.openweathermap.org/data/2.5/weather',
            params={'q': city, 'appid': api_key, 'units': 'metric'}
        )
        data = response.json()
        if response.status_code != 200:
            return jsonify({'error': data.get('message', 'Error fetching data')}), response.status_code
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
