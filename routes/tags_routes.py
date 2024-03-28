from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

tags_bp = Blueprint('tags_bp', __name__)

@tags_bp.route('/')
def index():
    # Lógica para exibir todas as tags
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM tags')
    rows = cursor.fetchall()
    conn.close()

    tags = [{'id': row[0], 'nome': row[1]} for row in rows]  # Criar lista de objetos de tag
    return render_template('tags.html', tags=tags)
    pass

@tags_bp.route('/add', methods=['POST'])
def add_tag():
    if request.method == 'POST':
        nome = request.form['nova_tag']  # Supondo que o formulário HTML tenha um campo 'nome'

        # Lógica para adicionar uma nova tag
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tags (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()

        # Redirecionamento após adicionar a tag
        return redirect(url_for('tags_bp.index'))  # Redirecionar para a página de exibição de todas as tags

    # Se a requisição não for do tipo POST, retornar um redirecionamento
    return redirect(url_for('tags_bp.index'))  # Redirecionar para a página de exibição de todas as tags
    pass

@tags_bp.route('/edit/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag(tag_id):
    # Lógica para editar uma tag
    if request.method == 'POST':
        # Se o formulário foi submetido
        novo_nome = request.form['novo_nome']  # Supondo que o formulário tenha um campo 'novo_nome'

        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tags SET nome = ? WHERE id = ?', (novo_nome, tag_id))
        conn.commit()
        conn.close()

        return redirect(url_for('tags_bp.index'))  # Redirecionar para a página de exibição de todas as tags após a edição

    else:
        # Se é uma requisição GET, exibir o formulário de edição
        conn = sqlite3.connect('links.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM tags WHERE id = ?', (tag_id,))
        tag = cursor.fetchone()
        conn.close()

        if tag:
            return render_template('edit_tag.html', tag_id=tag_id, nome=tag[0])
        else:
            # Se a tag com o ID especificado não existir, retornar uma mensagem de erro ou redirecionar para uma página de erro
            return 'Tag não encontrada', 404
    pass

@tags_bp.route('/delete/<int:tag_id>')
def delete_tag(tag_id):
    # Lógica para excluir uma tag
    conn = sqlite3.connect('links.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('tags_bp.index'))  # Redirecionar para a página de exibição de todas as tags após a exclusão
    pass
