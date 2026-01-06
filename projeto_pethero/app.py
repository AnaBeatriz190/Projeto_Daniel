from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pethero_secret_jg" # Necessário para mensagens de alerta (flash)

# 1. ROTA: HOME (Página Inicial com Vitrine)
@app.route('/')
def index():
    return render_template('index.html')

# 2. ROTA: LOGIN (Entrada do Protetor)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Captura os dados do formulário
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Lógica de validação (Futuro: Banco de Dados)
        print(f"Login realizado por: {email}")
        
        # Redireciona para o Painel do Protetor
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

# 3. ROTA: CADASTRO (Criação de conta de Herói)
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        print(f"Novo Herói cadastrado: {nome} ({email})")
        
        # Após cadastrar, envia para o Login
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')

# 4. ROTA: DASHBOARD (Painel de Gestão da Ana)
@app.route('/dashboard')
def dashboard():
    # Esta rota carrega o template image_fc7c48.jpg (Estatísticas e Mensagens)
    return render_template('dashboard.html')

# 5. ROTA: REPORTAR (Formulário de Resgate com Mapa)
@app.route('/reportar', methods=['GET', 'POST'])
def reportar():
    if request.method == 'POST':
        # Captura os dados do animal reportado
        especie = request.form.get('especie')
        descricao = request.form.get('descricao')
        
        print(f"Novo reporte de animal: {especie}")
        
        # Após reportar, volta para o Dashboard ou Home
        return redirect(url_for('dashboard'))
        
    return render_template('reportar.html')

# 6. ROTA: LOGOUT (Sair do Sistema)
@app.route('/logout')
def logout():
    return redirect(url_for('index'))

# 7. ROTA: DETALHES DO PET (Exemplo de rota dinâmica futura)
@app.route('/pet/<int:id>')
def detalhes_pet(id):
    # Aqui você mostraria detalhes de um animal específico
    return f"Visualizando detalhes do pet ID: {id}"

if __name__ == '__main__':
    # Roda em modo Debug para atualizar o site a cada mudança no código
    app.run(debug=True)