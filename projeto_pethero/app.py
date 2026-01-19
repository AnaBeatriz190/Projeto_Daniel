import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pethero_secret_jg_informatica"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pethero.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    cor = db.Column(db.String(50))
    condicao = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    foto = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Disponível')

# --- CARGA INICIAL DE DADOS (5 ANIMAIS PARA DEMONSTRAÇÃO) ---
with app.app_context():
    db.create_all()
    if Pet.query.count() == 0:
        pets_iniciais = [
            Pet(nome="Rex", especie="cachorro", idade=2, cor="Caramelo", descricao="Muito dócil e brincalhão.", status="Disponível"),
            Pet(nome="Luna", especie="gato", idade=1, cor="Cinza", descricao="Adora carinho e dormir no sol.", status="Disponível"),
            Pet(nome="Thor", especie="cachorro", idade=9, cor="Dourado", descricao="Calmo, ideal para companhia. (Idoso)", status="Disponível"),
            Pet(nome="Nina", especie="gato", idade=0, cor="Malhada", descricao="Energia pura! (Filhote)", status="Disponível"),
            Pet(nome="Bob", especie="cachorro", idade=4, cor="Preto", descricao="Leal e ótimo vigia.", status="Disponível")
        ]
        db.session.bulk_save_objects(pets_iniciais)
        db.session.commit()

@app.route('/')
def index():
    especie = request.args.get('especie')
    tipo = request.args.get('tipo')
    
    query = Pet.query
    if especie and especie != 'todos':
        query = query.filter_by(especie=especie)
    
    if tipo == 'filhotes':
        query = query.filter(Pet.idade <= 1)
    elif tipo == 'idosos':
        query = query.filter(Pet.idade >= 8)
        
    pets = query.all()
    return render_template('index.html', pets=pets)

@app.route('/voluntariar', methods=['GET', 'POST'])
def voluntariar():
    if request.method == 'POST':
        # Agora a mensagem aparece aqui e redireciona para cá
        flash("Cadastro realizado com êxito! Logo entraremos em contato. 🐾")
        return redirect(url_for('voluntariar'))
    return render_template('voluntariar.html')

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        novo = Pet(especie=request.form.get('especie'), cor=request.form.get('cor_principal'), descricao=request.form.get('descricao'))
        db.session.add(novo)
        db.session.commit()
        flash("Denúncia recebida com sucesso!")
        return redirect(url_for('reportar'))
    return render_template('reportar.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', pets=Pet.query.all())

@app.route('/sobre')
def sobre(): return render_template('sobre.html')

@app.route('/doar')
def doar(): return render_template('doar.html')

@app.route('/login')
def login(): return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)