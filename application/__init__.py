from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from datetime import datetime
import pandas as pd
import os



project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "kanban_db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = 'secret key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # redirect to "login" page if not logged yet

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

db = SQLAlchemy(app)
db.init_app(app)

"""
with app.app_context():
    from application import routes
    db.create_all()
    print('Database initialized!')

"""


# the class 'Model' is a declarative base used to declare models
class Task(db.Model):
    """ Task Model """
    __tablename__ = 'Task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description=db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return '<Title {}>'.format(self.title)

class User(UserMixin, db.Model):
    """ 'User Model' """
    __tablename__ ='User'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<Username {}>'.format(self.username)

db.create_all()
db.session.commit()

@app.route('/',  methods=['POST', 'GET'])
def home():
    return redirect('login')


@app.route('/board', methods=['POST', 'GET'])
@login_required
def show_board():
    todo = Task.query.filter_by(status=0).all()
    doing = Task.query.filter_by(status=1).all()
    done = Task.query.filter_by(status=2).all()

    return render_template('board.html', todo=todo, doing=doing, done=done)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/board")

    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
        if login_user is None:
            error = 'Your credentials are not correct. Try again'
            return render_template('login.html', error=error)
        login_user(user)
        #flash('Logged in successfully.')
        return redirect("/board")
    elif request.method=='GET':
        return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        new_user = User(username=request.form['username'],password=request.form['password'], email= request.form['email'])
        db.session.add(new_user)
        db.session.commit()
        #flash("You have successfully signed up for your Kanban Board!")
        return redirect("/login")
    elif request.method == 'GET':
        return render_template('signup.html')


@app.route("/add", methods=["GET", "POST"])
def addtask():
    if request.method == 'POST':
        new_task = Task(title=request.form['title'],description=request.form['description'],status=request.form['status'],deadline=pd.to_datetime(request.form['deadline']),user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        #flash("New task successfully added to your to-do!")
        return redirect("/board")
    elif request.method == 'GET':
        return render_template('add_task.html',title="Add Task")

@app.route('/todo/<int:id>', methods=['POST', 'GET'])
def todo(id):
    task=Task.query.get(id)
    task.status=0
    db.session.commit()
    flash(f'Task {task.title} has been placed in "To Do"')
    return redirect("/board")

@app.route('/doing/<int:id>', methods=['POST', 'GET'])
def doing(id):
    task=Task.query.get(id)
    task.status=1
    db.session.commit()
    flash(f'Task {task.title} has been placed in "Doing"')
    return redirect("/board")


@app.route('/done/<int:id>', methods=['POST', 'GET'])
def done(id):
    task=Task.query.get(id)
    task.status=2
    db.session.commit()
    flash(f'Task {task.title} has been placed in "Done"')
    return redirect("/board")

@app.route('/delete', methods=['POST'])
def delete():
    title = request.form.get('title')
    task=Task.query.filter_by(title=title).first()
    db.session.delete(task)
    db.session.commit()
    flash(f'Task {task.title} has been deleted')
    return redirect("/board")

@app.route('/task/<int:id>', methods=['POST', 'GET'])
@login_required
def task():
    id = request.form.get('id')
    task = Task.query.get(id).first()
    return render_template('task.html', task=task)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect('/board')


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    app.run(debug=True)
