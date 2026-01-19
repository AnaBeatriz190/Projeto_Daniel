import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pethero_secret_jg_informatica"

# Configuração do Banco de Dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pethero.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Pet
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    cor = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    foto = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Disponível')

# Criação automática dos dados de demonstração
with app.app_context():
    db.create_all()
    if Pet.query.count() == 0:
        pets_demo = [
            Pet(nome="Rex", especie="cachorro", idade=2, cor="Caramelo", foto="https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?q=80&w=500", descricao="Dócil e brincalhão."),
            Pet(nome="Luna", especie="gato", idade=1, cor="Cinza", foto="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=500", descricao="Adora carinho."),
            Pet(nome="Thor", especie="cachorro", idade=9, cor="Dourado", foto="https://images.unsplash.com/photo-1552053831-71594a27632d?q=80&w=500", descricao="Calmo e companheiro (Idoso)."),
            Pet(nome="Nina", especie="gato", idade=0, cor="Malhada", foto="https://images.unsplash.com/photo-1513245533132-aa7f8e72620f?q=80&w=500", descricao="Muito ativa! (Filhote)"),
            Pet(nome="Bob", especie="cachorro", idade=4, cor="Preto", foto="https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?q=80&w=500", descricao="Ótimo vigia.")
        ]
        db.session.bulk_save_objects(pets_demo)
        db.session.commit()

# --- ROTAS ---

@app.route('/')
def index():
    esp = request.args.get('especie')
    tipo = request.args.get('tipo')
    query = Pet.query
    if esp: query = query.filter_by(especie=esp)
    if tipo == 'filhotes': query = query.filter(Pet.idade <= 1)
    if tipo == 'idosos': query = query.filter(Pet.idade >= 8)
    return render_template('index.html', pets=query.all())

# ROTA DE CADASTRO (A que estava dando erro!)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Aqui você salvaria o usuário no banco futuramente
        flash("Conta criada com sucesso! Agora você pode fazer o login.")
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        flash("A equipe agradece o seu reporte!")
        return redirect(url_for('reportar'))
    return render_template('reportar.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', pets=Pet.query.all())

@app.route('/voluntariar', methods=['GET', 'POST'])
def voluntariar():
    if request.method == 'POST':
        flash("Cadastro realizado com êxito! Logo entraremos em contato. 🐾")
        return redirect(url_for('voluntariar'))
    return render_template('voluntariar.html')

@app.route('/sobre')
def sobre(): return render_template('sobre.html')

@app.route('/doar')
def doar(): return render_template('doar.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)