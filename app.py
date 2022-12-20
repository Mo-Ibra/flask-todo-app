from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


# Create new todo
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect("/")
        except:
            return 'Something went wrong'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


# Delete todo
@app.route('/delete/<int:id>')
def delete(id):

    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong.'

# Update todo
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    
    else:
        return render_template('update.html', task=task_to_update)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
