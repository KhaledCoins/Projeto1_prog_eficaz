'''Uma função para cada rota: monta as páginas e altera as anotações.'''

import utils


def index():
    '''Monta a página principal com o formulário e a lista de anotações.'''
    note_template = utils.load_template('components/note.html')
    notes_li = [
        note_template.format(
            id=note.id,
            title=utils.escape_html(note.title),
            details=utils.escape_html(note.content),
            star_class='on' if note.favorite else 'off',
            star_icon='★' if note.favorite else '☆',
            star_label='Desfavoritar' if note.favorite else 'Favoritar',
        )
        for note in utils.load_notes()
    ]
    notes = '\n'.join(notes_li)

    return utils.load_template('index.html').format(notes=notes)


def update_form(note_id):
    '''Monta a página de edição, ou devolve None se a anotação não existir.'''
    note = utils.load_note(note_id)
    if note is None:
        return None

    return utils.load_template('update.html').format(
        id=note.id,
        title=utils.escape_html(note.title),
        details=utils.escape_html(note.content),
    )


def submit(titulo, detalhes):
    '''Cria uma nova anotação.'''
    utils.save_note(titulo, detalhes)


def update(note_id, titulo, detalhes):
    '''Salva as alterações feitas em uma anotação.'''
    utils.update_note(note_id, titulo, detalhes)


def delete(note_id):
    '''Apaga uma anotação.'''
    utils.delete_note(note_id)


def favorite(note_id):
    '''Favorita ou desfavorita uma anotação.'''
    utils.toggle_favorite(note_id)
