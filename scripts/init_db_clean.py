from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, MetaData


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
    requisitado = db.Column(db.String(1), default='N')

class Socio(db.Model):
    __tablename__ = 'socio'
    cc = db.Column(db.Integer, primary_key=True)
    nome_soc = db.Column(db.String(150))
    email = db.Column(db.String(50))
    data_n = db.Column(db.String(10))
    morada = db.Column(db.String(150))
    ano_inscri = db.Column(db.Integer)
    ativo = db.Column(db.String(1))

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
    completo = db.Column(db.String(1), default='S')


class Socio_Camp(db.Model):
    __tablename__ = 'socio_camp'
    id_sc = db.Column(db.Integer, primary_key=True)
    id_camp_sc = db.Column(db.Integer, db.ForeignKey('campanha.id_camp'))
    cc_sc = db.Column(db.Integer, db.ForeignKey('socio.cc'))
    novo = db.Column(db.String(1))

if __name__ == "__main__":
	db.create_all()