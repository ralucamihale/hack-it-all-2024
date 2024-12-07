import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Used for session management

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_mentor = db.Column(db.Boolean, default=False)  # Additional field for mentors/users

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save user to database
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Log the user in
        session['user_id'] = new_user.id
        return redirect(url_for('main_page_logged_in'))

    return render_template('register_user.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main_page'))

# Dummy event data
events_data = [
    {"slug": "event1", "title": "Music Festival", "description": "A great outdoor music festival!"},
    {"slug": "event2", "title": "Art Exhibition", "description": "Explore local and international art."},
    {"slug": "event3", "title": "Tech Meetup", "description": "Discuss the latest trends in technology."},
]

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/logged_in')
def main_page_logged_in():
    return render_template('main_page_logged_in.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find user by email
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Log the user in
            return redirect(url_for('main_page_logged_in'))
        else:
            return "Invalid credentials", 401

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
    
@app.route('/events/create')
def create_event():
    # if request.method == 'POST':
    #     # Retrieve form data
    #     title = request.form['title']
    #     owner = request.form['owner']
    #     date = request.form['date']
    #     time = request.form['time']
    #     location = request.form['location']
    #     tags = request.form['tags']
    #     description = request.form['description']
    #     participants = request.form['participants']

    #     return "Event Created Successfully!"
    return render_template('create_event.html')

@app.route('/register_mentor')
def register_mentor():
    return render_template('register_mentor.html')

#@app.route('/register_user')
#def register_user():
#    return render_template('register_user.html')



def open_browser():
    webbrowser.open("http://127.0.0.1:8080/")

if __name__ == '__main__':
    open_browser()
    app.run(port=8080)
