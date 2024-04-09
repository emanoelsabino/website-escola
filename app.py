from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "1qaz2wsx3edc"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db"
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def get_user(user_id):
    return Usuario.query.filter_by(id=user_id).first()


class Professor(db.Model):
    __tablename__ = 'professor'
    id_professor = db.Column(db.Integer, primary_key=True)
    nome_professor = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nome_professor: str, turma: str) -> None:
        self.nome_professor = nome_professor
        self.turma = turma


class Aluno(db.Model):
    __tablename__ = 'aluno'
    
    id_aluno = db.Column(db.Integer, primary_key=True)
    nome_aluno = db.Column(db.String(100), nullable=False)
    nome_pai = db.Column(db.String(100), nullable=False)
    contato_pai = db.Column(db.String(100))
    nome_mae = db.Column(db.String(100), nullable=False)
    contato_mae = db.Column(db.String(100))
    professor = db.Column(db.String(100), nullable=False)
    
    def __init__(self, nome_aluno: str, nome_pai: str, nome_mae: str, contato_pai: str, contato_mae: str, professor: str) -> None:
        self.nome_aluno = nome_aluno
        self.nome_pai = nome_pai
        self.nome_mae = nome_mae
        self.contato_pai = contato_pai
        self.contato_mae = contato_mae
        self.professor = professor


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    
    def __init__(self, nome: str, senha: str, email: str) -> None:
        self.nome = nome
        self.senha = generate_password_hash(senha)
        self.email = email
    
    def verifica_senha(self, senha):
        return check_password_hash(self.senha, senha)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        try:
            usuario = Usuario(nome, senha, email)
            db.session.add(usuario)
            db.session.commit()
        except:
            print('erro')
        return render_template("register.html")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            return redirect("/login")
        elif not Usuario.verifica_senha(usuario, senha):
            return redirect("/login")
        
        login_user(usuario)
        return redirect("/")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/sobre")
def sobre():
    total_turmas = db.session.query(Professor.turma).distinct().count()
    total_professores = db.session.query(Professor.id_professor).distinct().count()
    total_alunos = db.session.query(Aluno.id_aluno).distinct().count()
    return render_template('sobre.html', total_turmas=total_turmas, total_alunos=total_alunos, total_professores=total_professores)

@app.route("/listar_professores")
def listar_professores():
    professores = db.session.execute(db.select(Professor)).scalars()
    return render_template('professores.html', professores=professores)

@app.route("/cadastrar_professor", methods=["GET", "POST"])
def cadastrar_professor():
    if request.method == "POST":
        status = {'type': 'sucesso', 'message': 'Professor cadastrado com sucesso!'}
        dados = request.form
        
        try:
            professor = Professor(dados['nome_professor'], dados['turma'])
            db.session.add(professor)
            db.session.commit()
            
            print(dados['nome_professor'])
            print(dados['turma'])
        except:
            status = {'type': 'erro', 'message': 'Ops! Erro ao realizar o cadastro.'}
        
        return render_template("cadastrar_professor.html", status=status)
    else:
        return render_template("cadastrar_professor.html")
    
@app.route("/editar_professor/<int:id_professor>", methods=["GET", "POST"])
def editar_professor(id_professor):
    if request.method == "POST":
        dados_editados = request.form
        professor = db.session.execute(db.select(Professor).filter(Professor.id_professor == id_professor)).scalar()
        
        professor.nome_professor = dados_editados['nome_professor']
        professor.turma = dados_editados['turma']
        
        db.session.commit()
        return redirect("/listar_professores")
    else:
        professor = db.session.execute(db.select(Professor).filter(Professor.id_professor == id_professor)).scalar()
        return render_template("editar_professor.html", professor=professor)

@app.route("/deletar_professor/<int:id_professor>")
def deletar_professor(id_professor):
    flash('Professor excluido com sucesso!')
    try:
        professor_deletado = db.session.execute(db.select(Professor).filter(Professor.id_professor == id_professor)).scalar()
        db.session.delete(professor_deletado)
        db.session.commit()
    except:
        flash('Erro ao excluir o Professor!')
    return redirect("/listar_professores")

@app.route("/listar_alunos")
def listar_alunos():
    alunos = db.session.execute(db.select(Aluno)).scalars()
    professores = db.session.execute(db.select(Professor)).scalars()
    professor_map = {professor.nome_professor: professor for professor in professores}
    return render_template('alunos.html', alunos=alunos, professor_map=professor_map)

@app.route("/detalhes_aluno/<int:id_aluno>")
def detalhes_aluno(id_aluno):
    aluno = db.session.execute(db.select(Aluno).filter(Aluno.id_aluno == id_aluno)).scalar()
    return render_template('detalhes_aluno.html', aluno=aluno)

@app.route("/cadastrar_aluno", methods=["GET", "POST"])
def cadastrar_aluno():
    professores = db.session.execute(db.select(Professor)).scalars()
    if request.method == "POST":
        status = {'type': 'sucesso', 'message': 'Aluno cadastrado com sucesso!'}
        dados = request.form
        
        try:
            aluno = Aluno(
                dados['nome_aluno'],
                dados['nome_pai'],
                dados['nome_mae'],
                dados['contato_pai'],
                dados['contato_mae'],
                dados['professor']
            )
            db.session.add(aluno)
            db.session.commit()
        except:
            status = {'type': 'erro', 'message': 'Ops! Erro ao realizar o cadastro.'}
        
        return render_template("cadastrar_aluno.html", status=status)
    else:
        return render_template("cadastrar_aluno.html", professores=professores)

@app.route("/editar_aluno/<int:id_aluno>", methods=["GET", "POST"])
def editar_aluno(id_aluno):
    professores = db.session.execute(db.select(Professor)).scalars()
    
    if request.method == "POST":
        dados_editados = request.form
        aluno = db.session.execute(db.select(Aluno).filter(Aluno.id_aluno == id_aluno)).scalar()
        
        aluno.nome_aluno = dados_editados['nome_aluno']
        aluno.nome_pai = dados_editados['nome_pai']
        aluno.nome_mae = dados_editados['nome_mae']
        aluno.contato_pai = dados_editados['contato_pai']
        aluno.contato_mae = dados_editados['contato_mae']
        aluno.professor = dados_editados['professor']
        
        db.session.commit()
        return redirect("/listar_alunos")
    else:
        aluno = db.session.execute(db.select(Aluno).filter(Aluno.id_aluno == id_aluno)).scalar()
        return render_template("editar_aluno.html", aluno=aluno, professores=professores)

@app.route("/deletar_aluno/<int:id_aluno>")
def deletar_aluno(id_aluno):
    flash('Aluno excluido com sucesso!')
    try:
        aluno_deletado = db.session.execute(db.select(Aluno).filter(Aluno.id_aluno == id_aluno)).scalar()
        db.session.delete(aluno_deletado)
        db.session.commit()
    except:
        flash('Erro ao excluir o Aluno!')
    return redirect("/listar_alunos")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        status = {'type': 'sucesso', 'message': 'Obrigado pelo contato. Mensagem enviada com sucesso!'}
        try:
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            print(name, email, message)
        except:
            status = {'type': 'erro', 'message': 'Ops! Houve um erro ao enviar a mensagem.'}
            print(status)
        
        return render_template("contato.html", status=status)
    else:
        return render_template('contato.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=80, debug=True)
