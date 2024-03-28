from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3

links_bp = Blueprint('links_bp', __name__)

# TODO Remove the palavra_chave database and include a new column in the links database to store the Connection required, related to a new table pre requirements 
@links_bp.route('/')
def index():
    format = request.args.get('format', default='html')  # Obtém o parâmetro 'format', padrão para 'html' se não estiver presente
    # Lógica para exibir todas as links
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, url, descricao, palavras_chave FROM links')
    rows = cursor.fetchall()
    conn.close()

    links = [{'id': row[0], 'url': row[1], 'descricao': row[2].replace('\n', ' '), 'palavras_chave': row[3]} for row in rows] # Criar lista de objetos de link
    if format == 'json':
        return jsonify(links)  # Retorna os dados no formato JSON
    
    return render_template('links.html', links=links)
    pass

@links_bp.route('/add',  methods=['GET', 'POST'])
def add_link():
    if request.method == 'POST':
        url = request.form['url'] 
        descricao = request.form['descricao'] 
        palavras_chave = request.form['palavras_chave'] 

        # Lógica para adicionar uma nova link
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO links (url, descricao, palavras_chave) VALUES ( ?, ?, ?)', (url, descricao, palavras_chave,))
        conn.commit()
        conn.close()

        # Redirecionamento após adicionar a link
        return redirect(url_for('links_bp.index'))  # Redirecionar para a página de exibição de todas as links

    # Se a requisição não for do tipo POST, retornar um redirecionamento
    return redirect(url_for('links_bp.index'))  # Redirecionar para a página de exibição de todas as links
    pass

@links_bp.route('/edit/<int:link_id>', methods=['GET', 'POST'])
def edit_link(link_id):
    # Lógica para editar uma link
    if request.method == 'POST':
        # Se o formulário foi submetido
        nova_url = request.form['nova_url'] 
        nova_descricao = request.form['nova_descricao'] 
        nova_palavras_chave = request.form['nova_palavras_chave'] 

        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE links SET url = ?, descricao = ?, palavras_chave = ? WHERE id = ?', (nova_url, nova_descricao, nova_palavras_chave, link_id,)) # Corrigir a query SQL
        
        conn.commit()
        conn.close()

        return redirect(url_for('links_bp.index'))  # Redirecionar para a página de exibição de todas as links após a edição

    else:
        # Se é uma requisição GET, exibir o formulário de edição
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, url, descricao, palavras_chave  FROM links WHERE id = ?', (link_id,))
        link = cursor.fetchone()
        conn.close()

        if link:
            return render_template('edit_link.html', link_id=link_id, url=link[1] , descricao=link[2], palavras_chave=link[3])
        else:
            # Se a link com o ID especificado não existir, retornar uma mensagem de erro ou redirecionar para uma página de erro
            return 'link não encontrada', 404
    pass

@links_bp.route('/delete/<int:link_id>')
def delete_link(link_id):
    # Lógica para excluir uma link
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM links WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('links_bp.index'))  # Redirecionar para a página de exibição de todas as links após a exclusão
    pass
