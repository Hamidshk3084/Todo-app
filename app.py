from flask import Flask, render_template ,url_for, request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer , default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("Form data:", request.form)  # Debugging
        task_content = request.form['content'] 
        print("Task content:", task_content)  # Debugging
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            print("Task added to session.")
            db.session.commit()
            print("Session committed.")
            return redirect('/')
        except Exception as e:
            print("Error committing task:", e)
            return 'There was an issue adding your task'
        
        


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route('/delete/<int:id>' , methods = ['GET', 'POST'])
def delete(id):
    print(f"Delete route triggered for ID: {id}")  # Debugging
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        print(f"Task with ID {id} deleted from session.")  # Debugging
        db.session.commit()
        print(f"Task with ID {id} committed to database.")  # Debugging
        return redirect('/')
    except Exception as e:
        print(f"Error while deleting task: {e}")
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    print(f"task with ID {id} updated from the session") #debugging
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue updating the task'
    else:
        return render_template('update.html' , task=task)




if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.create_all()
        print("Database created successfully!")
    app.run(debug=True)
