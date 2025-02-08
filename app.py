import csv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

deleted_flight_numbers = []
# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = 'Ru£[N9MZ:QQk]849$)2BY~JPHLh2oyYfT~'
login_manager = LoginManager(app)

# Define Flight class
class Flight:
    def __init__(self, **kwargs):
        self.details = kwargs

    def display_info(self):
        return self.details
    
# Define CancelledFlight subclass inheriting from Flight
class CancelledFlight(Flight):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_info(self):
        cancelled_info = super().display_info()
        cancelled_info['status'] = 'Cancelled'
        return cancelled_info

# Define User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Define filename and columns for flights data
filename = 'flights.csv'
columns = ['YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER', 'TAIL_NUMBER',
           'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME',
           'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME',
           'AIR_TIME', 'DISTANCE', 'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME',
           'ARRIVAL_DELAY', 'DIVERTED', 'CANCELLED', 'CANCELLATION_REASON', 'AIR_SYSTEM_DELAY',
           'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']

# Function to read flights data from CSV and filter cancelled flights
def read_and_filter_cancelled_flights(filename):
    cancelled_flights = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['CANCELLED'] == '1':  
                cancelled_flights.append(row)
    return sorted(cancelled_flights, key=lambda x: (x['YEAR'], x['MONTH'], x['DAY']))

# Function to display flight information
def display_flight_info(flight):
    return flight.display_info()

# Function to read flights data from CSV
def read_flights_data(filename):
    flights_data = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            flights_data.append(row)
    return flights_data

# Function to search flights based on given criteria
def search_flights(flights_data, criteria):
    result_flights = []
    for flight in flights_data:
        match = all(flight[key] == value or not value for key, value in criteria.items())
        if match and flight['FLIGHT_NUMBER'] not in deleted_flight_numbers:
            result_flights.append(flight)
    return result_flights

# Function to delete a flight from flights data
# Function to delete flights matching any of the flight numbers from flights data
def delete_flight(flights_data, flight_numbers_to_delete):
    deleted_flight_numbers.extend(flight_numbers_to_delete)
    updated_flights_data = [flight for flight in flights_data 
                            if flight['FLIGHT_NUMBER'] not in flight_numbers_to_delete]
    return updated_flights_data


# Function to add a new flight to flights data
def add_flight(new_flight):
    flights_data.append(new_flight)
    write_to_csv(filename, flights_data)

# Function to write flights data to CSV file
def write_to_csv(filename, flights_data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(flights_data)

# Function to merge two sorted data structures
def merge_sorted_data(data1, data2):
    merged_data = []
    i = j = 0
    while i < len(data1) and j < len(data2):
        if (int(data1[i]['YEAR']), int(data1[i]['MONTH']), int(data1[i]['DAY'])) < \
           (int(data2[j]['YEAR']), int(data2[j]['MONTH']), int(data2[j]['DAY'])):
            merged_data.append(data1[i])
            i += 1
        else:
            merged_data.append(data2[j])
            j += 1
    merged_data.extend(data1[i:])
    merged_data.extend(data2[j:])
    return merged_data

##### Flask Routes #####

# Route for user login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# Route for home page
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# Route for index page
@app.route('/index')
def index():
    return render_template('index.html')

# Route for flight search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_criteria = {}
        for column in columns:
            value = request.form.get(column, '').strip()
            search_criteria[column] = value

        search_results = search_flights(flights_data, search_criteria)
        if not search_results:
            return render_template('search_results.html', results=None)
        return render_template('search_results.html', results=search_results)
    return render_template('search.html', columns=columns)

# Route for displaying cancelled flights
@app.route('/cancelled_flights')
def cancelled_flights():
    cancelled_flights_data = read_and_filter_cancelled_flights(filename)
    return render_template('cancelled_flights.html', flights=cancelled_flights_data)

# Route for adding a new flight
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        new_flight = {}
        for column in columns:
            new_value = request.form.get(column, '')
            new_flight[column] = new_value

        add_flight(new_flight)
        return render_template('add_success.html')

    return render_template('add.html', columns=columns)

# Route for displaying delete flight page
@app.route('/delete_page', methods=['GET', 'POST'])
def delete_page():
    if request.method == 'POST':
        return redirect(url_for('delete'))
    return render_template('delete.html', columns=columns)

# Route for deleting a flight
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        flight_to_delete = {}
        for column in columns:
            value = request.form.get(column, '').strip()
            flight_to_delete[column] = value

        flights_data = read_flights_data(filename)
        updated_flights_data = delete_flight(flights_data, flight_to_delete)

        if updated_flights_data == flights_data:
            flash('Flight not found. No changes made.', 'error')
        else:
            write_to_csv(filename, updated_flights_data)
            flash('Flight deleted successfully!', 'success')

        return redirect(url_for('index'))

    return render_template('delete.html', columns=columns)

if __name__ == "__main__":
    flights_data = read_flights_data(filename)
    app.run(debug=True)
