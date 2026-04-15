from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
# The secret key is required to encrypt the session cookie
app.secret_key = 'ahsndjfidjeushdyshdjfk3ks'

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)')
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    # --- Session Logic ---
    # Increment a 'visits' counter stored only in the user's browser session
    session['visits'] = session.get('visits', 0) + 1

    # --- SQL / Database Logic ---
    if request.method == 'POST':
        new_note = request.form.get('note')
        if new_note:
            with sqlite3.connect('database.db') as conn:
                conn.execute('INSERT INTO notes (content) VALUES (?)', (new_note,))
        return redirect('/')

    # Fetch all notes to display
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT content FROM notes')
        all_notes = cursor.fetchall()

    return render_template('index.html', visits=session['visits'], notes=all_notes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)