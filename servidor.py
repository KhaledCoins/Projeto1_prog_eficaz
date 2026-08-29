from flask import Flask, abort, redirect, render_template_string, request

import utils
import views

app = Flask(__name__)

# Configurando a pasta de arquivos estáticos
app.static_folder = 'static'

# Garante que a tabela de anotações exista antes da primeira requisição
utils.init_db()


@app.route('/')
def index():

    return render_template_string(views.index())


@app.route('/submit', methods=['POST'])
def submit_form():
    titulo = request.form.get('titulo', '')  # Obtém o valor do campo 'titulo'
    detalhes = request.form.get('detalhes', '')  # Obtém o valor do campo 'detalhes'

    views.submit(titulo, detalhes)
    return redirect('/')


@app.route('/update/<int:note_id>')
def update_form(note_id):
    page = views.update_form(note_id)
    if page is None:
        abort(404)

    return render_template_string(page)


@app.route('/update', methods=['POST'])
def update_note():
    note_id = request.form.get('id', type=int)
    titulo = request.form.get('titulo', '')
    detalhes = request.form.get('detalhes', '')

    views.update(note_id, titulo, detalhes)
    return redirect('/')


@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    views.delete(note_id)
    return redirect('/')


@app.route('/favorite/<int:note_id>')
def favorite_note(note_id):
    views.favorite(note_id)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
