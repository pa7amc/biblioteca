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
    
    campanha1 = Campanha(nome_camp='Literatura Espanhola')
    campanha2 = Campanha(nome_camp='Literatura Sueca')
    campanha3 = Campanha(nome_camp='Por todo o mundo...')
    campanha4 = Campanha(nome_camp='Literatura Estrangeira')
    db.session.add(campanha1)
    db.session.add(campanha2)
    db.session.add(campanha3)
    db.session.add(campanha4)

    livro1 = Livro(ISBN=9789720033109, titulo='O Retrato de Dorian Gray', autor='Oscar Wilde', editora='Porto Editora', ano=2020, requisitado='N')
    livro2 = Livro(ISBN=9789896445409, titulo='Sapiens', autor='Yuval Noah Harari ', editora='Vintage Publishing,', ano=2015, requisitado='N')
    livro3 = Livro(ISBN=9789896232245, titulo='Pequena Escola do Pensamento Filosofico', autor='Karl Jaspers ', editora='Cavalo de Ferro', ano=2016, requisitado='N')
    livro4 = Livro(ISBN=9781788162609, titulo='Lives Of The Stoics', autor='Stephen Hanselman e Ryan Holiday ', editora='Profile Books Ltd', ano=2020, requisitado='N')
    livro5 = Livro(ISBN=9789722537919, titulo='O Corpo: Um Guia para Ocupantes', autor='Bill Bryson', editora='Bertrand Editora', ano=2019, requisitado='S')
    db.session.add(livro1)
    db.session.add(livro2)
    db.session.add(livro3)
    db.session.add(livro4)
    db.session.add(livro5)

    socio1 = Socio(cc=12345678, nome_soc='Carolina Santos', email='cs@gmail.com', data_n='03/07/1990', morada='Rua do Parque 7, 7300-456', ano_inscri=2021, ativo='S')
    socio2 = Socio(cc=12345679, nome_soc='Tiago Silva', email='ts@gmail.com', data_n='22/02/1997', morada='Estrada das Flores 1, 7200-898', ano_inscri=2019, ativo='N')
    socio3 = Socio(cc=12345676, nome_soc='Rita Calado', email='rc@hotmail.com', data_n='09/12/2000', morada='Rua das Amoreiras, lote 13, 2 esquerdo, 7400-784', ano_inscri=2020, ativo='S')
    socio4 = Socio(cc=87654321, nome_soc='Rui Oliveira', email='ro@hotmail.com', data_n='29/05/1987', morada='Bairro do Olival 23, 7000-345', ano_inscri=2020, ativo='S')
    socio5 = Socio(cc=12648300, nome_soc='Gisela Pereira', email='gp@gmail.com', data_n='01/01/1980', morada='Beco dos Descobrimentos 7, 7900-300', ano_inscri=2021, ativo='N')
    db.session.add(socio1)
    db.session.add(socio2)
    db.session.add(socio3)
    db.session.add(socio4)
    db.session.add(socio5)


    req1 = Requisito(ISBN_req=9789722537919, cc_req=12345678, data_req='24/01/2021', data_entr='02/02/2021', completo='N')
    req2 = Requisito(ISBN_req=9781788162609, cc_req=12345676, data_req='20/01/2021', data_entr='28/01/2021', completo='S')
    db.session.add(req1)
    db.session.add(req2)

    adesao1 = Socio_Camp(id_camp_sc=1, cc_sc=12648300, novo='S')
    adesao2 = Socio_Camp(id_camp_sc=3, cc_sc=12345676, novo='N')
    db.session.add(adesao1)
    db.session.add(adesao2)


    db.session.commit()