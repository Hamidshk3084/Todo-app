from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime, timedelta



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# Task model with new due_date field
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.DateTime, nullable=True)  # NEW

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, "%Y-%m-%dT%H:%M") if due_date_str else None
        new_task = Task(content=content, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')

    tasks = Task.query.order_by(Task.date_created.desc()).all()

    # Calculate progress
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.completed])
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks else 0

    return render_template('index.html', tasks=tasks, now=datetime.utcnow(), progress=progress, timedelta=timedelta)


@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', task=task)

@app.route('/toggle/<int:id>')
def toggle(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
