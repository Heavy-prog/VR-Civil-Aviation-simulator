from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random
from flask_cors import CORS

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///performance_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# Database models for the tables
class PerformanceOverview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_hours = db.Column(db.Integer, nullable=False)
    total_flights = db.Column(db.Integer, nullable=False)
    completed_simulations = db.Column(db.Integer, nullable=False)
    unsuccessful_simulations = db.Column(db.Integer, nullable=False)

class FlightData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flight_type = db.Column(db.String(50), nullable=False)  # 'success' or 'failure'
    value = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(100), nullable=False)

class AircraftDamage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    damage_type = db.Column(db.String(100), nullable=False)
    damage_value = db.Column(db.Integer, nullable=False)

# Initialize the database (if tables do not exist)
with app.app_context():
    db.create_all()

# Routes to fetch data
@app.route('/api/performance-overview', methods=['GET'])
def get_performance_overview():
    overview = PerformanceOverview.query.first()
    if not overview:
        # Generate default data
        overview = PerformanceOverview(
            flight_hours=50,
            total_flights=120,
            completed_simulations=100,
            unsuccessful_simulations=20
        )
        db.session.add(overview)
        db.session.commit()

    return jsonify({
        'flight_hours': overview.flight_hours,
        'total_flights': overview.total_flights,
        'completed_simulations': overview.completed_simulations,
        'unsuccessful_simulations': overview.unsuccessful_simulations
    })

@app.route('/api/successful-flights', methods=['GET'])
def get_successful_flights():
    time_period = request.args.get('time_period', 'monthly')
    flights = FlightData.query.filter_by(flight_type='success').all()
    if not flights:
        # Generate random data if no records
        sample_data = {
            'success': [random.randint(60, 100) for _ in range(5)],
            'labels': ['Flight 1', 'Flight 2', 'Flight 3', 'Flight 4', 'Flight 5']
        }
        for value, label in zip(sample_data['success'], sample_data['labels']):
            new_flight = FlightData(flight_type='success', value=value, label=label)
            db.session.add(new_flight)
        db.session.commit()
        flights = FlightData.query.filter_by(flight_type='success').all()

    return jsonify({
        'labels': [flight.label for flight in flights],
        'success': [flight.value for flight in flights]
    })

@app.route('/api/unsuccessful-flights', methods=['GET'])
def get_unsuccessful_flights():
    time_period = request.args.get('time_period', 'monthly')
    airplane_model = request.args.get('airplane_model', 'all')
    flights = FlightData.query.filter_by(flight_type='failure').all()
    if not flights:
        # Generate random data if no records
        sample_data = {
            'failure': [random.randint(20, 50) for _ in range(5)],
            'labels': ['Flight 1', 'Flight 2', 'Flight 3', 'Flight 4', 'Flight 5']
        }
        for value, label in zip(sample_data['failure'], sample_data['labels']):
            new_flight = FlightData(flight_type='failure', value=value, label=label)
            db.session.add(new_flight)
        db.session.commit()
        flights = FlightData.query.filter_by(flight_type='failure').all()

    return jsonify({
        'labels': [flight.label for flight in flights],
        'failure': [flight.value for flight in flights]
    })

@app.route('/api/aircraft-damage', methods=['GET'])
def get_aircraft_damage():
    time_period = request.args.get('time_period', 'monthly')
    airplane_model = request.args.get('airplane_model', 'Boeing 737')
    damage_data = AircraftDamage.query.all()
    if not damage_data:
        # Generate random damage data
        sample_data = {
            'labels': ['Wing', 'Tail', 'Engine', 'Landing Gear', 'Fuselage'],
            'damage': [random.randint(0, 10) for _ in range(5)]
        }
        for damage_type, damage_value in zip(sample_data['labels'], sample_data['damage']):
            new_damage = AircraftDamage(damage_type=damage_type, damage_value=damage_value)
            db.session.add(new_damage)
        db.session.commit()
        damage_data = AircraftDamage.query.all()

    return jsonify({
        'labels': [damage.damage_type for damage in damage_data],
        'damage': [damage.damage_value for damage in damage_data]
    })

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
