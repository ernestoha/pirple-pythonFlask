from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
        return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
        return render_template('about.html')

@app.route('/terms-of-use', methods=['GET'])
def termsOfUse():
        return render_template('terms-of-use.html')

@app.route('/privacy', methods=['GET'])
def privacy():
        return render_template('privacy.html')

@app.route('/sign-up', methods=['GET'])
def signUp():
        return render_template('sign-up.html')

@app.route('/log-in', methods=['GET'])
def logIn():
        return render_template('log-in.html')

@app.route('/dashboard', methods=['GET'])
def dashBoard():
        return render_template('dashboard.html')

@app.route('/todo-new', methods=['GET'])
def todoNew():
        return render_template('todo-new.html')

@app.route('/todo-edit', methods=['GET'])
def todoEdit():
        return render_template('todo-edit.html')

@app.route('/user-edit', methods=['GET'])
def userEdit():
        return render_template('user-edit.html')

if __name__ == '__main__':
        app.run(host = "0.0.0.0", port = 7000, debug = True)
