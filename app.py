from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            new_note = Note(content=content)
            db.session.add(new_note)
            db.session.commit()
        return redirect(url_for('index'))
    search = request.args.get('search', '')
    if search:
        notes = Note.query.filter(Note.content.contains(search)).order_by(Note.timestamp.desc()).all()
    else:
        notes = Note.query.order_by(Note.timestamp.desc()).all()
    return render_template('index.html', notes=notes, search=search)

@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    note.content = request.form['edited_content']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
