from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask.helpers import get_flashed_messages
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = 'YUFGf74uyG76 TFr78TY0JYG5'


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
        flash("NO NOTE WITH THAT ID")
        return redirect(url_for('home'))
        

@app.route('/edit', methods=['GET', 'POST'])
def edit_note():
    if request.method == 'GET':
        code = request.args.get('code')
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE code = ?', (code,))
        note = cursor.fetchone()
        conn.close()

        if note:
            # Store the 'code' value in the session
            session['code'] = code
            return render_template('edit_note.html', note=note)
        else:
            return 'Note not found', 404
    elif request.method == 'POST':
        # Retrieve the 'code' value from the session
        code = session.get('code')
        if code is None:
            return 'Note not found', 404

        # Handle the POST request to save the edited note
        content = request.form['content']
        
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE notes SET content = ? WHERE code = ?', (content, code))
        conn.commit()
        conn.close()

        return redirect(url_for('view_note', code=code))  # Redirect to the view page after saving




if __name__ == '__main__':
    app.run(debug=True)
