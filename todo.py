from flask import * 
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,current_user, login_user,logout_user, login_required
from forms import RegisterForm, LoginForm
from flask_login import UserMixin

conn = sqlite3.connect('todo_data.db')
print("Opened database successfully")

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\ASUS\\Documents\\intership\\todo_data1.db'
app.config['SECRET_KEY'] = "abc123"    
login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    task = db.relationship('Tasks', backref='user')


    def __repr__(self):
        return f'User{self.first_name}{self.email}'

@login_manager.user_loader
def load_user(id):
   return User.query.get(int(id))
#    return User.query.filter(User.id == int(user_id)).first()

class Tasks(db.Model):
   id = db.Column('task_id', db.Integer, primary_key = True)
   task = db.Column(db.String(100))
   description = db.Column(db.String(50))
   status = db.Column(db.String(255))
   todo_owner = db.Column(db.Integer,db.ForeignKey('user.id'))

def __init__(self, task, description):
   self.task = task
   self.description = description


@app.route('/', methods = ['POST','GET'])
@app.route('/home', methods = ['POST','GET'])
def home():
    return render_template('home_todo.html')


@app.route('/register', methods = ['POST','GET'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if request.method == 'POST':
        if form.validate_on_submit:
            user = User(first_name =form.first_name.data,
                        last_name =form.last_name.data,
                        email =form.email.data,
                        password = generate_password_hash(form.password.data)
                        )
            exists = db.session.query(db.session.query(User).filter_by(email=form.email.data).exists()).scalar()
            if exists:
               msg= 'Email already registered!'
               return render_template('register.html', form=form,msg=msg)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
           


@app.route('/login', methods = ['POST','GET'])
def login():
   form = LoginForm()
   msg=''
   if form.validate_on_submit:
      user = User.query.filter_by(email = form.email.data).first()
      if user and check_password_hash(user.password, form.password.data):
         login_user(user)
         return redirect('/index')
      else:
         msg="Invalid details"
   return render_template('login_todo.html', form=form,msg=msg)


@app.route('/logout', methods = ['POST','GET'])
def logout():
    logout_user()
    return redirect('/home')

@app.route('/index', methods = ['POST','GET'])
def index_todo():
    id1 = current_user.id
    tasksu = Tasks.query.filter_by(todo_owner = id1)
    tsklst=list(tasksu)
    return render_template("index_todo.html",tasks = tasksu,tsklst=tsklst)

@app.route('/addtask',methods=['GET','POST'])
def addtask():
    user=current_user  
    if request.method == 'GET':
        return render_template('index_todo.html')
    
    if request.method=='POST':   
      fstatus = request.form.getlist('chkstatus')
      if fstatus== []:
         status = 'Not Completed'
      else:
         status = 'Completed'
         
      taskadd = Tasks(task=request.form['task'],description=request.form['description'],status=status,todo_owner = user.id)        
      db.session.add(taskadd)
      db.session.commit()
      flash('Record was successfully added')
      return redirect(url_for('index_todo'))

@app.route('/updatestatus/<int:id>',methods = ['GET','POST'])    
def updatestatus(id):
    user=current_user
    if request.method == 'GET': 
       task =Tasks.query.filter_by(id =id,todo_owner = current_user.id).first()
       statusu=task.status
       print(task.status)
       if statusu=='Completed':
          statusu='Not Completed'
       else:
          statusu='Completed'   
       task.status=statusu 
       db.session.commit()
    return redirect('/index') 



@app.route('/edit/<int:id>',methods = ['GET','POST'])
def update(id):
   user = current_user
   if request.method == 'POST': 
      fstatus = request.form.getlist('chkstatus')
      if fstatus== []:
         status = 'Not Completed'
      else:
         status = 'Completed'
      task =Tasks.query.filter_by(id =id,todo_owner = current_user.id).first()
      task.task=request.form['task']
      task.description=request.form['description']
      task.status=status
      db.session.commit()
   return redirect('/index')


   #    updtskid =tasks.query.filter_by(id=id).first()
   #    task=request.form['updtask']
   #    description=request.form['upddescripyion']
   #    setattr(updtskid,task,description)
   #    taskuadd = tasks(task,description)
   #    db.session.add(taskuadd)
   #    db.session.commit()
   # return render_template('index_todo.html',tasks=tasks.query.all())
    # taskupdate = tasks.query.get_or_404(id)

    # if request.method == 'POST':
    #     taskupdate.content = request.form['task']

    #     try:
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return 'There was an issue while updating that task'

    # else:
    #     return render_template('task_update.html', task=taskupdate)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def deletetask(id):
   Tasks.query.filter_by(id=id,todo_owner = current_user.id).delete()
   db.session.commit()
   return redirect('/index')

@app.route('/users')
def users():
    users = User.query.all()
    print(users)

    res = {}
    for user in users:
        res = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password':user.password

        }
    return jsonify(res)

if(__name__)=='__main__':
   #  app.before_request(self._load_user)
    with app.app_context():
      db.create_all()
    app.run(debug=True)


# import sqlite3
# from sqlite3 import Error


# def create_connection(db_file):
#     """ create a database connection to a SQLite database """
#     conn = None
#     try:
#         conn = sqlite3.connect('todo_data.db')
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

