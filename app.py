from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Intanciando o banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///escola.db"
db = SQLAlchemy()
db.init_app(app)


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


@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/listar_alunos")
def listar_alunos():
    alunos = db.session.execute(db.select(Aluno)).scalars()
    professores = db.session.execute(db.select(Professor)).scalars()
    professor_map = {professor.nome_professor: professor for professor in professores}
    return render_template('alunos.html', alunos=alunos, professor_map=professor_map)

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
