from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "ef0cc4d3880644acbd65f6218a3beed6"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    if request.method == 'POST':
        city = request.form['city']
        from urllib.parse import quote_plus
        city_encoded = quote_plus(city)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('main') and data.get('weather'):
                weather = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon']
                }
            else:
                weather = {'error': data.get('message', 'Weather data not found')}
        else:
            try:
                error_message = response.json().get('message', 'City not found')
            except Exception:
                error_message = 'City not found'
            weather = {'error': error_message}
    return render_template('index.html', weather=weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
