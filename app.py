from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

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

@app.route('/register_mentor')
def register_mentor():
    return render_template('register_mentor.html')

@app.route('/register_user')
def register_user():
    return render_template('register_user.html')



def open_browser():
    webbrowser.open("http://127.0.0.1:8080/")

if __name__ == '__main__':
    open_browser()
    app.run(port=8080)
