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

class Dividas(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    valor=db.Column(db.Integer())
    dia=db.Column(db.Integer())
    mes=db.Column(db.Integer())
    ano=db.Column(db.Integer())
    userid=db.Column(db.Integer())
    descricao=db.Column(db.String(100),nullable=False)

class Lucros(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    valor=db.Column(db.Integer())
    dia=db.Column(db.Integer())
    mes=db.Column(db.Integer())
    ano=db.Column(db.Integer())
    userid=db.Column(db.Integer())
    descricao=db.Column(db.String(100),nullable=False)

class cores(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    foreground=db.Column(db.String(10),default="#ffffff")
    background=db.Column(db.String(10),default="#101010")
    panelbgcolor=db.Column(db.String(10),default="#404040")
    mainbg=db.Column(db.String(10),default="#a7acb5")
    panelmenubgcolor=db.Column(db.String(10),default="#665a78")
    userid=db.Column(db.Integer())

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
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
    # NOTE: variaveis de cor que serao pegas na db
    foreground="white"
    background="#101010"
    panelbgcolor="#404040"
    mainbg="#a7acb5"
    panelmenubgcolor="#665a78"
    colortemplate=f"""
    :root {{
      --login-page-bg: {background};
      --login-page-fg: {foreground};
      --panel-bgcolor:{panelbgcolor};
      --mainbg:{mainbg};
      --panel-menubgcolor:{panelmenubgcolor};
    }}
    """
    response = make_response(colortemplate,200)
    response.mimetype = "text/css"
    return response

@app.route('/entradas')
def entradas():
    user_id=current_user.id
    dados=Lucros.query.filter_by(userid=user_id).all()  
    return render_template("entradas.html",dados=dados)
@app.route('/api/',methods=['POST'])
@login_required 
def api():
    print(request.data)
    data = request.get_json()
    user_id = current_user.id
    type=data.get("type")
    if type=="profit":
        dados=Lucros.query.filter_by(userid=user_id).all()
        print(dados);
        dados_serializaveis = []
        for lucro in dados:
            lucro_dict = {
            'id': lucro.id,
            'userid': lucro.userid,
            'valor': lucro.valor,
            'dia':lucro.dia,
            'mes':lucro.mes,
            'ano':lucro.ano,
            'desc':lucro.descricao
            }
            dados_serializaveis.append(lucro_dict)
        response = jsonify(dados_serializaveis)
    else:
        response=jsonify("404")
    return response





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
