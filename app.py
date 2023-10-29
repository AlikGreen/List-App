from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT,
        content TEXT
    )
''')
conn.commit()
conn.close()

# Function to generate a unique note code (you can improve this logic)
def generate_note_code():
    import uuid
    return str(uuid.uuid4())[:6]

# Create a new note
@app.route('/create', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        content = request.form['content']
        code = generate_note_code()
        
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (code, content) VALUES (?, ?)', (code, content))
        conn.commit()
        conn.close()
        
        return redirect(url_for('get_note', code=code))
    
    return render_template('create_note.html')

# Retrieve a note by code
@app.route('/<code>')
def get_note(code):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE code = ?', (code,))
    note = cursor.fetchone()
    conn.close()
    
    if note:
        return render_template('note.html', note=note)
    else:
        return 'Note not found', 404

# Edit a note by code
@app.route('/edit/<code>', methods=['GET', 'POST'])
def edit_note(code):
    if request.method == 'GET':
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE code = ?', (code,))
        note = cursor.fetchone()
        conn.close()

        if note:
            return render_template('edit_note.html', note=note)
        else:
            return 'Note not found', 404
    elif request.method == 'POST':
        content = request.form['content']
        
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET content = ? WHERE code = ?', (content, code))
        conn.commit()
        conn.close()

        return redirect(url_for('get_note', code=code))

if __name__ == '__main__':
    app.run(debug=True)
