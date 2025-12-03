import sqlite3
from flask import g, current_app

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config.get('DATABASE', 'foods.db'))
        g.db.row_factory = sqlite3.Row  # Para acessar colunas por nome (opcional, mas útil)
        # Habilita WAL para melhor concorrência (reduz locks)
        g.db.execute('PRAGMA journal_mode=WAL;')
        g.db.execute('PRAGMA synchronous=NORMAL;')  # Otimização para performance
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    try:
        db.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT,
            password_hash TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT,
            description TEXT,
            image_url TEXT
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS favorites (
            user_id INTEGER,
            food_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(food_id) REFERENCES foods(id),
            PRIMARY KEY(user_id, food_id)
        )''')
        # Popula com dados de exemplo (20 comidas: 10 originais + 10 novas)
        foods = [
            # Comidas originais (10)
            ('Feijoada', 'Brasil', 'Comida feita com carinho', 'img/feijoada.webp'),
            ('Pão de Queijo', 'Brasil', 'Comida feita com carinho', 'img/paodequeijo.jpg'),
            ('Moqueca', 'Brasil', 'Comida feita com carinho', 'img/moqueca.jpg'),
            ('Churrasco', 'Brasil', 'Comida feita com carinho', 'img/churrasco.jpg'),
            ('Lasanha', 'Itália', 'Comida feita com carinho', 'img/lasanha.jpg'),
            ('Tiramisu', 'Itália', 'Comida feita com carinho', 'img/Tiramisù.jpg'),
            ('Pizza', 'Itália', 'Comida feita com carinho', 'img/pizza.jpg'),
            ('Torta Al Testo', 'Itália', 'Comida feita com carinho', 'img/tortaaltesto.jpg'),
            ('Sushi', 'Japão', 'Comida feita com carinho', 'img/sushi.jpg'),
            ('Tacos', 'México', 'Comida feita com carinho', 'img/tacos.jpg'),
            # Novas 10 comidas
            ('Brigadeiro', 'Brasil', 'Doce brasileiro cremoso feito com chocolate e leite condensado.', 'img/brigadeiro.jpg'),
            ('Coxinha', 'Brasil', 'Salgado frito recheado com frango e catupiry.', 'img/coxinha.jpg'),
            ('Risotto', 'Itália', 'Arroz cremoso cozido lentamente com caldo e ingredientes variados.', 'img/risotto.jpg'),
            ('Pasta Carbonara', 'Itália', 'Massa com ovos, queijo pecorino e pancetta.', 'img/carbonara.jpg'),
            ('Tempura', 'Japão', 'Frutos do mar ou vegetais fritos em massa leve.', 'img/tempura.jpg'),
            ('Ramen', 'Japão', 'Macarrão japonês em caldo rico, com toppings variados.', 'img/ramen.jpg'),
            ('Guacamole', 'México', 'Molho cremoso feito com abacate, limão e temperos.', 'img/guacamole.jpg'),
            ('Enchiladas', 'México', 'Tortilhas recheadas com carne ou queijo, cobertas com molho.', 'img/enchiladas.jpg'),
            ('Acarajé', 'Brasil', 'Bolinho de feijão frito, típico da Bahia.', 'img/acaraje.jpg'),
            ('Onigiri', 'Japão', 'Bolinhos de arroz recheados, envoltos em alga nori.', 'img/onigiri.jpg'),
        ]
        for food in foods:
            db.execute('INSERT OR IGNORE INTO foods (name, country, description, image_url) VALUES (?, ?, ?, ?)', food)
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        print(f"Erro ao inicializar DB: {e}")
        raise

def add_user(username, email, password_hash):
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash))
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        print(f"Erro ao adicionar usuário: {e}")
        raise  # Re-lança o erro para o Flask lidar

def get_user(username):
    db = get_db()
    try:
        cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None

def get_foods(country='', sort='name_asc', search=''):
    db = get_db()
    try:
        query = 'SELECT * FROM foods'
        params = []
        conditions = []
        if country:
            conditions.append('country = ?')
            params.append(country)
        if search:
            conditions.append('name LIKE ?')
            params.append('%' + search + '%')
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        if sort == 'name_asc':
            query += ' ORDER BY name ASC'
        elif sort == 'name_desc':
            query += ' ORDER BY name DESC'
        cursor = db.execute(query, params)
        foods = cursor.fetchall()
        return foods
    except sqlite3.Error as e:
        print(f"Erro ao buscar comidas: {e}")
        return []

def search_foods(query):
    db = get_db()
    try:
        cursor = db.execute('SELECT * FROM foods WHERE name LIKE ?', ('%' + query + '%',))
        foods = cursor.fetchall()
        return foods
    except sqlite3.Error as e:
        print(f"Erro ao buscar comidas: {e}")
        return []

def add_favorite(user_id, food_id):
    db = get_db()
    try:
        db.execute('INSERT OR IGNORE INTO favorites (user_id, food_id) VALUES (?, ?)', (user_id, food_id))
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        print(f"Erro ao adicionar favorito: {e}")
        raise

def remove_favorite(user_id, food_id):
    db = get_db()
    try:
        db.execute('DELETE FROM favorites WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        db.commit()
    except sqlite3.Error as e:
        db.rollback()
        print(f"Erro ao remover favorito: {e}")
        raise

def get_favorites(user_id):
    db = get_db()
    try:
        cursor = db.execute('''SELECT f.id, f.name, f.country, f.description, f.image_url FROM foods f
                     JOIN favorites fav ON f.id = fav.food_id WHERE fav.user_id = ?''', (user_id,))
        favs = cursor.fetchall()
        return favs
    except sqlite3.Error as e:
        print(f"Erro ao buscar favoritos: {e}")
        return []

def is_favorite(user_id, food_id):
    db = get_db()
    try:
        cursor = db.execute('SELECT 1 FROM favorites WHERE user_id = ? AND food_id = ?', (user_id, food_id))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Erro ao checar favorito: {e}")
        return False