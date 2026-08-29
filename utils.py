'''Funções auxiliares do Get-it: acesso ao banco de dados e aos templates.'''

import html
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / 'banco.db'
TEMPLATES_DIR = BASE_DIR / 'static' / 'templates'


@dataclass
class Note:
    '''Uma anotação do Get-it.'''

    id: int
    title: str
    content: str
    favorite: bool = False


@contextmanager
def connect():
    '''Abre uma conexão com o banco, salvando as alterações ao final.'''
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db():
    '''Cria a tabela de anotações caso ela ainda não exista.'''
    with connect() as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                favorite INTEGER NOT NULL DEFAULT 0
            )
        ''')


def build_note(row):
    '''Converte uma linha do banco de dados em um objeto do tipo Note.'''
    return Note(
        id=row['id'],
        title=row['title'],
        content=row['content'],
        favorite=bool(row['favorite']),
    )


def load_notes():
    '''Devolve todas as anotações, com as favoritas em primeiro lugar.'''
    with connect() as connection:
        rows = connection.execute(
            'SELECT id, title, content, favorite FROM note '
            'ORDER BY favorite DESC, id'
        ).fetchall()

    return [build_note(row) for row in rows]


def load_note(note_id):
    '''Devolve a anotação com o id informado, ou None caso ela não exista.'''
    with connect() as connection:
        row = connection.execute(
            'SELECT id, title, content, favorite FROM note WHERE id = ?',
            (note_id,),
        ).fetchone()

    return build_note(row) if row else None


def save_note(title, content):
    '''Insere uma nova anotação no banco de dados.'''
    with connect() as connection:
        connection.execute(
            'INSERT INTO note (title, content) VALUES (?, ?)',
            (title, content),
        )


def update_note(note_id, title, content):
    '''Atualiza o título e o conteúdo de uma anotação existente.'''
    with connect() as connection:
        connection.execute(
            'UPDATE note SET title = ?, content = ? WHERE id = ?',
            (title, content, note_id),
        )


def delete_note(note_id):
    '''Apaga do banco de dados a anotação com o id informado.'''
    with connect() as connection:
        connection.execute('DELETE FROM note WHERE id = ?', (note_id,))


def toggle_favorite(note_id):
    '''Favorita a anotação, ou a desfavorita caso ela já seja favorita.'''
    with connect() as connection:
        connection.execute(
            'UPDATE note SET favorite = NOT favorite WHERE id = ?',
            (note_id,),
        )


def load_template(name):
    '''Devolve o conteúdo do template com o nome informado.'''
    return (TEMPLATES_DIR / name).read_text(encoding='utf-8')


def escape_html(text):
    '''Escapa um texto do usuário para inseri-lo com segurança no HTML.

    Além dos caracteres especiais do HTML, as chaves também são escapadas
    porque os templates são montados com .format() e renderizados pelo Flask.
    '''
    return html.escape(text).replace('{', '&#123;').replace('}', '&#125;')
