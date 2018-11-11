from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
#luego de instalar flask-sqlalchemy con pip y de importarlo aquí, tengo que decirle a sqlalchemy
#cuál base de datos voy a usar. Eso lo haré un poco más abajo.
from flask_sqlalchemy import SQLAlchemy
#Aquí importo desde el módulo forms.py que creé en esta misma carpeta:
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
#la cadena randómica, en realidad él la generó así:
#import secrets (en la línea de comando) y luego: secrets.token_hex(16)
app.config['SECRET_KEY']='unacadenarandomica'
#las tres slashes en este caso significan: relative path from current file:
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#cada clase es una tabla de la base de datos:
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Usuario('{self.username}','{self.email}','{self.image_file}') "

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey='user.id', nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


db=SQLAlchemy(app)

posts=[
    { 'autor':'Borges', 'título':'Ficciones'
    },
    { 'autor':'Dolina', 'título':'Cartas Marcadas'
    }
]

@app.route('/')
@app.route('/home')
def pagina_de_home():
    return render_template('home.html', posts_en_template=posts)

@app.route('/about')
def pagina_de_about():
    return render_template('about.html', title='acerca de...')

#Atenti al parámetro methods que hay que pasarle al formulario para que ande:
@app.route('/registrate', methods=['GET', 'POST'])
def funcion_del_registro():
    instancia_formulario_de_registro = RegistrationForm()
    #recordar que para que aparezcan los mensajes "flash" invocados a continuación,
    #  hay que llamarlos en layout.html. "Success" es clase css de Bootstrap
    if instancia_formulario_de_registro.validate_on_submit():
        flash(f'Cuenta creada para {instancia_formulario_de_registro.username.data}', 'success')
        return redirect(url_for('pagina_de_home'))
    return render_template('registrate.html', title='registro', formulario=instancia_formulario_de_registro)

#Atenti al parámetro methods que hay que pasarle al formulario para que ande:
@app.route('/logueate', methods=['GET', 'POST'])
def funcion_del_logueo():
    instancia_formulario_de_logueo = LoginForm()    
    #recordar que para que aparezcan los mensajes "flash" invocados a continuación,
    #  hay que llamarlos en layout.html. "Success" es clase css de Bootstrap
    if instancia_formulario_de_logueo.validate_on_submit():
#####OJO QUE ACÁ ME ESTÁ FALTANDO TODAVÍA UN CONDICIONAL
        '''     if los datos son correctos...
            flash('Has ingresado a tu cuenta', 'success')
            return redirect(url_for('pagina_de_home'))
        else:
            flash('La embarraste. Probá de nuevo', 'danger')'''
    return render_template('logueate.html', title='Logueate', formulario=instancia_formulario_de_logueo)


if __name__=='__main__':
    app.run(debug=True)