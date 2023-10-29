from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import uuid

app = Flask(__name__)

# Create a new SQLite database or connect to an existing one
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

# Function to generate a unique note code
def generate_note_code():
    while True:
        code = str(uuid.uuid4())[:6]
        # Check if the code already exists in the database
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT code FROM notes WHERE code = ?', (code,))
        existing_code = cursor.fetchone()
        conn.close()
        if not existing_code:
            return code

@app.route('/')
def home():
    return render_template('index.html')

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
        
        return redirect(url_for('view_note', code=code))
    
    return render_template('create_note.html')

@app.route('/view')
def view_note():
    code = request.args.get('code')
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE code = ?', (code,))
    note = cursor.fetchone()
    conn.close()

    if note:
        return render_template('view_note.html', note=note)
    else:
        return 'Note not found', 404

@app.route('/edit')
def edit_note():
    code = request.args.get('code')
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM notes WHERE code = ?', (code,))
    note = cursor.fetchone()
    conn.close()

    if note:
        return render_template('edit_note.html', note=note)
    else:
        return 'Note not found', 404

if __name__ == '__main__':
    app.run(debug=True)
