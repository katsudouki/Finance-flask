from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import datetime
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
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

class dividas(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor=db.Column(db.Integer())
    dia=db.Column(db.Integer())
    mes=db.Column(db.Integer())
    ano=db.Column(db.Integer())
    categoria=db.Column(db.String(100))
    pago=db.Column(db.String(100))
    userid=db.Column(db.Integer())
    descricao=db.Column(db.String(100),nullable=False)

class lucros(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    valor=db.Column(db.Integer())
    dia=db.Column(db.Integer())
    mes=db.Column(db.Integer())
    ano=db.Column(db.Integer())
    userid=db.Column(db.Integer())
    descricao=db.Column(db.String(100),nullable=False)
class categories(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    categoria=db.Column(db.String(20))

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
    dados=lucros.query.filter_by(userid=user_id).all()  
    return render_template("entradas.html",dados=dados)

@app.route('/saidas')
def saidas():
    user_id=current_user.id
    dados=dividas.query.filter_by(userid=user_id).all()  
    return render_template("saidas.html",dados=dados)
@app.route('/dash')
def dash():
    return render_template("dash.html")

@app.route('/configs')
def configs():
    user_id=current_user.id
    dados=dividas.query.filter_by(userid=user_id).all()  
    return render_template("config.html",dados=dados)

@app.route('/api/categories/',methods=['GET'])
def categ():
    dados=categories.query.all()  
    dadosjson=[]
    for dado in dados:
        dadosjson.append(dado.categoria)
    return jsonify(dadosjson)


@app.route('/api/', methods=['POST'])
@login_required 
def api():
    data = request.get_json()
    print(data)
    user_id = current_user.id
    tabela = data.get("tabela")
    tipo = data.get("type")
    
    if tipo == "insertlucro":
        id = data.get("id")
        valor = data.get("valor")
        dia = data.get("dia")
        mes = data.get("mes")
        ano = data.get("ano")
        desc = data.get("desc")

        if id == '0':
            # INFO: Inserir novo registro na tabela com user_id
            novo_lucro = lucros(valor=valor, dia=dia, mes=mes, ano=ano,descricao=desc,userid=user_id)
            db.session.add(novo_lucro)
            db.session.commit()
            response = jsonify({"message": "Novo registro inserido com sucesso"})
        else:
            # INFO: Atualizar registro existente na tabela
            lucro_existente = lucros.query.filter_by(id=id, userid=user_id).first()
            if lucro_existente:
                lucro_existente.valor = valor
                lucro_existente.dia = dia
                lucro_existente.mes = mes
                lucro_existente.ano = ano
                lucro_existente.descricao = desc
                db.session.commit()
                response = jsonify({"message": f"Registro com ID {id} atualizado com sucesso"})
            else:
                response = jsonify({"message": "Registro não encontrado para atualização"})
    if tipo == "insertpreju":
        id = data.get("id")
        valor = data.get("valor")
        dia = data.get("dia")
        mes = data.get("mes")
        ano = data.get("ano")
        categ = data.get("categ")
        desc = data.get("desc")
        pago=str(data.get("pago")).lower()

        if id == '0':
            # INFO: Inserir novo registro na tabela com user_id
             novo_preju = dividas(valor=valor, dia=dia, mes=mes, ano=ano, categoria=categ, descricao=desc, pago=pago, userid=user_id)
             db.session.add(novo_preju)
             db.session.commit()
             response = jsonify({"message": "Novo registro inserido com sucesso"})
        else:
            # INFO: Atualizar registro existente na tabela
            preju_existente = dividas.query.filter_by(id=id, userid=user_id).first()
            if preju_existente:
                preju_existente.valor = valor
                preju_existente.dia = dia
                preju_existente.mes = mes
                preju_existente.ano = ano
                preju_existente.categoria = categ
                preju_existente.pago = pago
                preju_existente.descricao = desc
                db.session.commit()
                response = jsonify({"message": f"Registro com ID {id} atualizado com sucesso"})
            else:
                response = jsonify({"message": "Registro não encontrado para atualização"})
    elif tipo == "delete":
        print("ue")
        id = data.get("id")
        # INFO: Executar a query de delete para a tabela especificada em 'tabela'
        tabela_query = globals().get(tabela)
        if tabela_query:
            registro = tabela_query.query.filter_by(id=id, userid=user_id).first()
            print(registro)
            if registro:
                db.session.delete(registro)
                db.session.commit()
                response = jsonify({"message": f"Registro com ID {id} deletado com sucesso"})
            else:
                response = jsonify({"message": f"Registro não encontrado para deleção na tabela {tabela}"})
        else:
            response = jsonify({"message": f"Tabela '{tabela}' não encontrada"})
    else:
        response = jsonify({"message": "404"})

    return response

@app.route('/dados/')
def obter_dados():
    # Obtém o ano atual
    ano_atual = datetime.datetime.now().year

    # Obtém os lucros e gastos do ano atual
    lucros_ano_atual = lucros.query.filter_by(ano=ano_atual).all()
    dividas_ano_atual = dividas.query.filter_by(ano=ano_atual).all()

    # Calcula os totais de lucros e gastos por mês
    lucros_por_mes = [0] * 12
    dividas_por_mes = [0] * 12
    for lucro in lucros_ano_atual:
        lucros_por_mes[lucro.mes - 1] += lucro.valor
    for divida in dividas_ano_atual:
        dividas_por_mes[divida.mes - 1] += divida.valor

    # Obtém os gastos das últimas 3 meses, do mês atual e dos próximos 3 meses
    mes_atual = datetime.datetime.now().month
    meses_para_considerar = [(mes_atual - 3 + i) % 12 + 1 for i in range(7)]
    gastos_por_categoria = {categoria: [0] * 7 for categoria in set([d.categoria for d in dividas_ano_atual])}
    for divida in dividas_ano_atual:
        if divida.mes in meses_para_considerar:
            gastos_por_categoria[divida.categoria][meses_para_considerar.index(divida.mes)] += divida.valor

    return jsonify({
        'lucros_por_mes': lucros_por_mes,
        'dividas_por_mes': dividas_por_mes,
        'gastos_por_categoria': gastos_por_categoria
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
