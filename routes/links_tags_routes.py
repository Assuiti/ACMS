from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import sqlite3

links_tags_bp = Blueprint('links_tags_bp', __name__)

@links_tags_bp.route('/')
def index():
    # Lógica para exibir todas as links_tags
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT links_tags.id, links_tags.link_id, links_tags.tag_id, links.palavras_chave, tags.nome
                      FROM links_tags
                   inner join links on links_tags.link_id = links.id
                   inner join tags on links_tags.tag_id = tags.id''')
    link_tag_rows = cursor.fetchall()

    cursor.execute('''SELECT id, palavras_chave FROM links''')
    link_rows = cursor.fetchall()

    cursor.execute('''SELECT id, nome FROM tags''')
    tag_rows = cursor.fetchall()

    conn.close()


    links_tags = [{'id': link_tag_row[0], 'link_id': link_tag_row[1], 'tag_id': link_tag_row[2], 'palavras_chave':link_tag_row[3], 'tagNome':link_tag_row[4]} for link_tag_row in link_tag_rows] # Criar lista de objetos de link_tag

    # Coletar todos os valores em uma lista separada
    links = [{'id': link_row[0], 'url': link_row[1]} for link_row in link_rows]  # Criar lista de pares id e url
    tags = [{'id': tag_row[0], 'nome': tag_row[1]} for tag_row in tag_rows] 

    return render_template('links_tags.html', rows=links_tags,links=links,tags=tags)

@links_tags_bp.route('/add',  methods=['GET', 'POST'])
def add_link_tag():
    if request.method == 'POST':
        link_id = request.form['link_id'] 
        tag_id = request.form['tag_id'] 

        # Lógica para adicionar uma nova link_tag
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO links_tags (link_id, tag_id) VALUES (?, ?)', (link_id, tag_id,))
        conn.commit()
        conn.close()

        # Redirecionamento após adicionar a link_tag
        return redirect(url_for('links_tags_bp.index'))  # Redirecionar para a página de exibição de todas as links_tags

    # Se a requisição não for do tipo POST, retornar um redirecionamento
    return redirect(url_for('links_tags_bp.index'))  # Redirecionar para a página de exibição de todas as links_tags

@links_tags_bp.route('/edit/<int:link_id>', methods=['GET', 'POST'])
def edit_link_tag(link_tag_id):
    # Lógica para editar uma link_tag
    if request.method == 'POST':
        link_id = request.form['link_id'] 
        tag_id = request.form['tag_id'] 

        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE links_tags SET link_id = ?, tag_id = ? WHERE id = ?', (link_id, tag_id, link_tag_id,))
        conn.commit()
        conn.close()

        return redirect(url_for('links_tags_bp.index'))  # Redirecionar para a página de exibição de todas as links_tags após a edição

    else:
        # Se é uma requisição GET, exibir o formulário de edição
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, link_id, tag_id FROM links_tags WHERE id = ?', (link_tag_id,))
        link_tag = cursor.fetchone()
        conn.close()

        if link_tag:
            return render_template('edit_link_tag.html', link_tag_id=link_tag_id, link_id=link_tag[1], tag_id=link_tag[2])
        else:
            # Se a link_tag com o ID especificado não existir, retornar uma mensagem de erro ou redirecionar para uma página de erro
            return 'link_tag não encontrada', 404

@links_tags_bp.route('/delete/<int:link_id>')
def delete_link_tag(link_id):
    # Lógica para excluir uma link_tag
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM links_tags WHERE id = ?', (link_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('links_tags_bp.index'))  # Redirecionar para a página de exibição de todas as links_tags após a exclusão
