from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import database as db
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_secreta'  # Mude para algo seguro em produção

# Adicionado: Registra o fechamento automático de conexões DB após cada requisição
app.teardown_appcontext(db.close_db)

@app.route('/')
def home():
    return render_template('index.html')  # Assumo que existe

@app.route('/comidas')
def comidas():
    return render_template('comidas.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('comidas'))
        return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        try:
            db.add_user(username, email, password)
            return redirect(url_for('login'))
        except Exception as e:
            # Adicionado: Tratamento básico de erro (ex.: usuário já existe)
            return render_template('cadastro.html', error=str(e))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/favoritos')
def favoritos():
    # Modificado: Não redireciona mais; passa variáveis para o template decidir o que mostrar
    user_logged_in = 'user_id' in session
    favorites = db.get_favorites(session.get('user_id', 0)) if user_logged_in else []
    return render_template('favoritos.html', user_logged_in=user_logged_in, favorites=favorites)

@app.route('/pesquisa')
def pesquisa():
    query = request.args.get('q', '').strip()
    if query:
        # Busca comidas por nome (case-insensitive)
        foods = db.search_foods(query)
        return render_template('comidas.html', search_query=query, foods=foods)  # Passa os resultados para o template
    return redirect(url_for('comidas'))  # Se não houver query, volta para comidas

@app.route('/api/comidas', methods=['GET'])
def api_comidas():
    country = request.args.get('country', '')
    sort = request.args.get('sort', 'name_asc')
    search = request.args.get('search', '')  # Novo parâmetro para pesquisa
    foods = db.get_foods(country=country, sort=sort, search=search)
    return jsonify([{'id': f[0], 'name': f[1], 'country': f[2], 'description': f[3], 'image': f[4]} for f in foods])

@app.route('/api/favoritar', methods=['POST'])
def api_favoritar():
    if 'user_id' not in session:
        return jsonify({'error': 'Não logado'}), 401
    data = request.get_json()
    food_id = data['food_id']
    action = data['action']  # 'add' ou 'remove'
    if action == 'add':
        db.add_favorite(session['user_id'], food_id)
    else:
        db.remove_favorite(session['user_id'], food_id)
    return jsonify({'success': True})

@app.route('/api/is_favorite', methods=['GET'])
def api_is_favorite():
    if 'user_id' not in session:
        return jsonify({'is_favorite': False}), 401
    food_id = request.args.get('food_id', type=int)
    if not food_id:
        return jsonify({'error': 'ID da comida necessário'}), 400
    is_fav = db.is_favorite(session['user_id'], food_id)
    return jsonify({'is_favorite': is_fav})

if __name__ == '__main__':
    # Modificado: Inicializa o DB dentro do contexto da aplicação para evitar erro de contexto
    with app.app_context():
        db.init_db()  # Cria banco e popula com dados
    app.run(debug=True)