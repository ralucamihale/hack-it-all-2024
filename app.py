from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import webbrowser

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    county = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Dummy event data
events_data = [
    {"slug": "event1", "title": "Music Festival", "description": "A great outdoor music festival!"},
    {"slug": "event2", "title": "Art Exhibition", "description": "Explore local and international art."},
    {"slug": "event3", "title": "Tech Meetup", "description": "Discuss the latest trends in technology."},
]

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        data = request.get_json()
        user_role = data.get('role', 'user')
        # Process other form data here
        print(f"User Role: {user_role}")  # Debugging
        if user_role == "mentor":
            return render_template('main_page_logged_in_mentor.html')
        else:
            return render_template('main_page.html')
    return render_template('main_page.html')
    

@app.route('/find_people')
def find_people():
    return render_template('find_people.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/events')
def events():
    return render_template('events.html', events=events_data)


@app.route('/events/<event_name>')
def event_detail(event_name):
    # Find the event by its slug
    event = next((e for e in events_data if e['slug'] == event_name), None)
    if event:
        return render_template('event_detail.html', event=event)
    else:
        return "Event not found", 404
    
@app.route('/events/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        # Get JSON data from the request
        event_data = request.get_json()

        # Add the event data to the events_data list
        new_event = {
            "slug": event_data['title'].lower().replace(" ", "_"),
            "title": event_data['title'],
            "description": event_data['description'],
        }
        events_data.append(new_event)

        # Respond with a success message
        return jsonify({"message": "Event created successfully!"})

    # Render the Create Event form
    return render_template('create_event.html')

@app.route('/register_mentor')
def register_mentor():
    return render_template('register_mentor.html')

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        occupation = request.form['occupation']
        nationality = request.form['role']
        county = request.form['role']
        interests = request.form['role']
        password = request.form['password']

        # Save the user to the database
        new_user = User(
            username=username,
            email=email,
            age=age,
            occupation=occupation,
            nationality=nationality,
            county=county,
            interests=interests,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main_page'))

    return render_template('register_user.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    # Retrieve form data
    username = request.form['username']
    email = request.form['email']
    age = request.form['age']
    occupation = request.form['occupation']
    nationality = request.form['role']
    county = request.form['role']
    interests = request.form['interests']
    password = request.form['password']

    # Save the data to the database
    new_user = User(
        username=username,
        email=email,
        age=age,
        occupation=occupation,
        nationality=nationality,
        county=county,
        interests=interests,
        password=password
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('main_page')) 

@app.route('/users')
def view_users():
    try:
        users = User.query.all()  # Query all users from the database
        return render_template('view_users.html', users=users)
    except Exception as e:
        return f"An error occurred: {e}", 500


def open_browser():
    webbrowser.open("http://127.0.0.1:8080/")

if __name__ == '__main__':
    open_browser()
    # db.create_all()
    app.run(port=8080)
