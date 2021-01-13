from flask import Flask, render_template, request
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Livro(db.Model):
    __tablename__ = 'livro'
    ISBN = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    autor = db.Column(db.String(70))
    editora = db.Column(db.String(70))
    ano = db.Column(db.Integer)
    requisitado = db.Column(db.String(2), default='N')

class Socio(db.Model):
    __tablename__ = 'socio'
    cc = db.Column(db.Integer, primary_key=True)
    nome_soc = db.Column(db.String(150))
    email = db.Column(db.String(50))
    data_n = db.Column(db.String(10))
    morada = db.Column(db.String(150))
    ano_inscri = db.Column(db.Integer)
    ativo = db.Column(db.String(2))

class Campanha(db.Model):
    __tablename__ = 'campanha'
    id_camp = db.Column(db.Integer, primary_key=True)
    nome_camp = db.Column(db.String(150))

class Requisito(db.Model):
    __tablename__ = 'requisito'
    id_req = db.Column(db.Integer, primary_key=True)
    ISBN_req = db.Column(db.Integer, db.ForeignKey('livro.ISBN'))
    cc_req = db.Column(db.Integer, db.ForeignKey('socio.cc'))
    data_req = db.Column(db.String(10))
    data_entr = db.Column(db.String(10))


class Socio_Camp(db.Model):
    __tablename__ = 'socio_camp'
    id_sc = db.Column(db.Integer, primary_key=True)
    id_camp_sc = db.Column(db.Integer, db.ForeignKey('campanha.id_camp'))
    cc_sc = db.Column(db.Integer, db.ForeignKey('socio.cc'))
    #se comecou a ser socio naquela campanha - true, senao - false
    novo = db.Column(db.String(2))





@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/campanhas', methods=['GET'])
def campanhas():
    return render_template('campanhas.html')


@app.route('/compl_req', methods=['GET'])
def compl_req():
    return render_template('compl_req.html')


@app.route('/reg_livro', methods=['GET'])
def reg_livro():
    return render_template('reg_livro.html')

@app.route('/reg_livro2', methods=['POST'])
def reg_livro2():
    ISBN = request.form.get('isbn', '')
    tit = request.form.get('tit', '')
    autor = request.form.get('autor', '')
    editora = request.form.get('edit', '')
    ano = request.form.get('ano', '')
    edicao = request.form.get('edi', '')

    livro = Livro(ISBN=ISBN, titulo=tit, autor=autor, editora=editora, ano=ano, requisitado='N')

    db.session.add(livro)
    db.session.commit()

    return render_template('sucesso.html')



@app.route('/reg_req', methods=['GET'])
def reg_req():
    return render_template('reg_req.html')


@app.route('/reg_soc', methods=['GET'])
def reg_soc():
    return render_template('reg_soc.html')

@app.route('/reg_soc2', methods=['POST'])
def reg_soc2():
    cc = request.form.get('cc', '')
    nome_soc = request.form.get('nome', '')
    email = request.form.get('email', '')
    data_n = request.form.get('dn', '')
    morada = request.form.get('morada', '')
    ano_inscri = request.form.get('ano_insc', '')
    ativo = request.form.get('status', '')

    socio = Socio(cc=cc, nome_soc=nome_soc, email=email, data_n=data_n, morada=morada, ano_inscri=ano_inscri, ativo=ativo)

    db.session.add(socio)
    db.session.commit()

    return render_template('sucesso.html')


@app.route('/ver_req', methods=['GET'])
def ver_req():
    return render_template('ver_req.html')


@app.route('/ver_soc', methods=['GET'])
def ver_soc():
    return render_template('ver_soc.html')







port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    import  Database.Tables.Livro
    import  Database.Tables.Socio
    import  Database.Tables.Campanha
    import  Database.Tables.Requisito
    import  Database.Tables.Socio_Camp

    db.create_all()
    app.run(host='0.0.0.0', port=port)