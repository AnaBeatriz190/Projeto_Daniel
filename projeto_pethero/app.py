import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pethero_secret_key_2026"

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pethero.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS ---
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    especie = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    cor = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    foto = db.Column(db.String(200))
    status = db.Column(db.String(20), default='DISPONÍVEL') 
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class PedidoAdocao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interessado = db.Column(db.String(100))
    pet_nome = db.Column(db.String(100))
    status = db.Column(db.String(20), default='PENDENTE') 
    data = db.Column(db.String(20), default=datetime.now().strftime("%d %b, %Y"))

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.String(100))
    conteudo = db.Column(db.Text)
    tempo = db.Column(db.String(20))

# --- REINICIALIZAÇÃO DO BANCO (5 ANIMAIS ORIGINAIS) ---
with app.app_context():
    db.drop_all() 
    db.create_all()
    
    pets_demo = [
        Pet(nome="Rex", especie="CACHORRO", idade=2, cor="Caramelo", foto="https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?q=80&w=500", descricao="Dócil e brincalhão.", status="DISPONÍVEL"),
        Pet(nome="Luna", especie="GATO", idade=1, cor="Cinza", foto="https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?q=80&w=500", descricao="Adora carinho.", status="DISPONÍVEL"),
        Pet(nome="Thor", especie="CACHORRO", idade=9, cor="Dourado", foto="https://images.unsplash.com/photo-1552053831-71594a27632d?q=80&w=500", descricao="Calmo e companheiro.", status="DISPONÍVEL"),
        Pet(nome="Nina", especie="GATO", idade=0, cor="Malhada", foto="https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?q=80&w=500", descricao="Muito ativa! (Filhote)", status="DISPONÍVEL"),
        Pet(nome="Bob", especie="CACHORRO", idade=4, cor="Preto", foto="https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?q=80&w=500", descricao="Ótimo vigia.", status="DISPONÍVEL")
    ]
    
    db.session.bulk_save_objects(pets_demo)
    db.session.add(PedidoAdocao(interessado="Sarah Costa", pet_nome="Rex", status="PENDENTE"))
    db.session.add(Mensagem(remetente="João Pedro", conteudo="Olá, o Rex se dá bem com gatos?", tempo="10min"))
    db.session.commit()

# --- ROTA HOME ---
@app.route('/')
def index():
    esp = request.args.get('especie')
    tipo = request.args.get('tipo')
    q = Pet.query.filter_by(status='DISPONÍVEL')
    if esp: q = q.filter(Pet.especie == esp.upper())
    if tipo == 'filhotes': q = q.filter(Pet.idade <= 1)
    if tipo == 'idosos': q = q.filter(Pet.idade >= 8)
    return render_template('index.html', pets=q.all())

# --- ROTA SOBRE (RESTAURADA) ---
@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# --- ROTAS DO DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    total = Pet.query.count()
    em_adocao = Pet.query.filter_by(status='DISPONÍVEL').count()
    adotados = Pet.query.filter_by(status='ADOTADO').count()
    pendentes = PedidoAdocao.query.filter_by(status='PENDENTE').count()
    pedidos = PedidoAdocao.query.order_by(PedidoAdocao.id.desc()).all()
    mensagens_lista = Mensagem.query.order_by(Mensagem.id.desc()).all()
    meus_pets = Pet.query.order_by(Pet.data_cadastro.desc()).all()
    return render_template('dashboard.html', total=total, em_adocao=em_adocao, adotados=adotados, pendentes=pendentes, pedidos=pedidos, mensagens=mensagens_lista, meus_pets=meus_pets)

@app.route('/mudar_status_pet/<int:id>/<novo_status>')
def mudar_status_pet(id, novo_status):
    pet = Pet.query.get_or_404(id)
    pet.status = novo_status.strip().upper()
    db.session.commit()
    flash(f"Status atualizado!", "dashboard")
    return redirect(url_for('dashboard'))

@app.route('/mudar_status_pedido/<int:id>/<novo_status>')
def mudar_status_pedido(id, novo_status):
    pedido = PedidoAdocao.query.get_or_404(id)
    pedido.status = novo_status.strip().upper()
    db.session.commit()
    flash(f"Pedido atualizado!", "dashboard")
    return redirect(url_for('dashboard'))

# --- ACESSO E FORMULÁRIOS ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        flash("Conta criada!", "cadastro")
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        flash("Denúncia enviada!", "reporte")
        return redirect(url_for('reportar'))
    return render_template('reportar.html')

@app.route('/doar', methods=['GET', 'POST'])
def doar():
    if request.method == 'POST':
        flash("Obrigado!", "doacao")
        return redirect(url_for('doar'))
    return render_template('doar.html')

@app.route('/voluntariar', methods=['GET', 'POST'])
def voluntariar():
    if request.method == 'POST':
        flash("Contato recebido!", "voluntario")
        return redirect(url_for('voluntariar'))
    return render_template('voluntariar.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        flash("E-mail enviado!", "recuperar")
        return redirect(url_for('login'))
    return render_template('recuperar.html')

@app.route('/pedidos')
def pedidos(): return render_template('pedidos_adocao.html', pedidos=PedidoAdocao.query.all())

@app.route('/mensagens')
def mensagens(): return render_template('mensagens.html', mensagens=Mensagem.query.all())

@app.route('/perfil')
def perfil(): 
    user_data = {"nome": "Ana Herói", "pets_resgatados": 42, "localizacao": "Cuité, PB", "bio": "Protetora dedicada."}
    return render_template('perfil.html', user=user_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)