from flask import Flask, redirect, render_template, request, jsonify, url_for
import subprocess
from geopy.geocoders import Nominatim

app = Flask(__name__)

# This list will store train information
trains = []

def get_coordinates(city_name, country="India"):
    geolocator = Nominatim(user_agent="train_tracker_app")
    location = geolocator.geocode(f"{city_name}, {country}")
    
    if location:
        return location.latitude, location.longitude
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_train', methods=['POST'])
def add_train():
    train_number = request.form['train_number']
    date = request.form['date']
    try:
        coordinates = get_coordinates(request.form['new_location'])
        if coordinates:
            train_info = {
                'train_number': train_number,
                'date': date,
                'new_location': request.form['new_location'],
                'coordinates': f'{coordinates[0]},{coordinates[1]}'
            }
            trains.append(train_info)
            return redirect(url_for('output_page'))
        else:
            return render_template('output.html', trains=trains, error_message='Invalid coordinates for station')
    except Exception as e:
        return render_template('output.html', trains=trains, error_message=str(e))

@app.route('/output')
def output_page():
    return render_template('output.html', trains=trains)

if __name__ == '__main__':
    app.run(debug=True)
