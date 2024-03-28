import sqlite3
from routes.tags_routes import tags_bp
from routes.links_routes import links_bp 
from routes.links_tags_routes import links_tags_bp 
from flask import Flask, render_template

app = Flask(__name__)


app.register_blueprint(tags_bp , url_prefix='/tags' )
app.register_blueprint(links_bp, url_prefix='/links')
app.register_blueprint(links_tags_bp, url_prefix='/links_tags')

@app.route('/')
def index():
    # Lógica para exibir todas as links
    # TODO: Create a DatabaseManager class to handle database connection
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, url, descricao, palavras_chave FROM links')
    rows = cursor.fetchall()
    conn.close()

    links = [{'id': row[0], 'url': row[1], 'descricao': row[2], 'palavras_chave': row[3]} for row in rows] # Criar lista de objetos de link
    return render_template('pagina_links.html', links=links)
if __name__ == '__main__':
    app.run(debug=True)
