from flask import Flask, render_template, request, redirect, url_for, session, flash,make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = 'secret2024kk@#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = username
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'danger')
    return render_template('index.html')

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# INFO: generate css variables with user defined colors   
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
