from flask import Flask, render_template, redirect, request
import requests
import json
import time


app = Flask(__name__)
URL = 'http://api.openweathermap.org/data/2.5/weather?q={town},bg&APPID={api_key}&units=metric'
api_key = '641f819b425303db04d4b83df3c7e042'


def get_details(url):
    return requests.get(url)


def convert_data_to_json(data):
    return json.loads(data.text)


def convert_time_sunrise_and_sunset(mytime):
    return time.ctime(mytime).split()[3]


@app.route('/', methods=['GET'])
def index():
    return render_template('get_city_info.html')


@app.route('/weather', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        town = request.form['town']
        FULL_URL = URL.format(town=town, api_key=api_key)
        json_details = {'message': 'Error'}
        data = get_details(FULL_URL)

        if data.status_code == 200:
            json_details = convert_data_to_json(data)
            if json_details['cod'] == 200:
                json_details['sys']['sunrise'] = convert_time_sunrise_and_sunset(
                    json_details['sys']['sunrise'])
                json_details['sys']['sunset'] = convert_time_sunrise_and_sunset(
                    json_details['sys']['sunset'])
                return render_template('index.html', data=json_details)
            else:
                return "<h3>Error with try to parse data from input town</h3>"

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
