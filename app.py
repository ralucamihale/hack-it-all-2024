from flask import Flask, render_template
import webbrowser

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/logged_in')
def main_page_logged_in():
    return render_template('main_page_logged_in.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/events')
def events():
    return render_template('events.html')

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
