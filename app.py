from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

app = Flask(__name__)
app.secret_key = 'secret2024kk@#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('home'))


@app.route('/auth', methods=['POST'])
def auth():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            response = {'message': 'True'}
            return redirect_with_json_response(url_for('dashboard'), response)
        else:
            response={'message':'False'}
            return make_response(jsonify(response), 200)

    return render_template('index.html')

def redirect_with_json_response(location, json_response):
    response = make_response(jsonify(json_response), 200)
    response.headers['Location'] = location
    return response

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/static/css/colorscheme.css')
def colorscheme():
    foreground="white"
    background="#101010"
    colortemplate=f"""
    :root {{
      --login-page-bg: {background};
      --login-page-fg: {foreground};
    }}
    """
    response = make_response(colortemplate,200)
    response.mimetype = "text/css"
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
