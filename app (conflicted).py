from flask import Flask, render_template, request
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy import create_engine, Table, MetaData


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
    completo = db.Column(db.String(1))


class Socio_Camp(db.Model):
    __tablename__ = 'socio_camp'
    id_sc = db.Column(db.Integer, primary_key=True)
    id_camp_sc = db.Column(db.Integer, db.ForeignKey('campanha.id_camp'))
    cc_sc = db.Column(db.Integer, db.ForeignKey('socio.cc'))
    #se comecou a ser socio naquela campanha - true, senao - false
    novo = db.Column(db.String(1))






@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

#Campanha
@app.route('/campanhas', methods=['GET'])
def campanhas():    
    campanhas = Campanha.query.all()
    return render_template('campanhas.html', campanhas=campanhas)


@app.route('/reg_camp', methods=['POST'])
def reg_camp():
    nome_campa = request.form.get('campa', '')
    campanha = Campanha(nome_camp=nome_campa)

    db.session.add(campanha)
    db.session.commit()

    return render_template('sucesso.html')


@app.route('/socio_camp', methods=['GET'])
def socio_camp():    
    campanhas = Campanha.query.all()
    socios = Socio.query.all()
    sc = Socio_Camp.query.all()
    return render_template('socio_camp.html', campanhas=campanhas, sc=sc, socios=socios)


@app.route('/socio_camp2', methods=['POST'])
def socio_camp2():    
    id_campa = request.form.get('campa', '')
    cc_campa = request.form.get('ccs', '')
    novo = request.form.get('novo', '')

    sc = Socio_Camp(id_camp_sc=id_campa, cc_sc=cc_campa, novo=novo)

    db.session.add(sc)
    db.session.commit()

    return render_template('sucesso.html')


#Requisito
@app.route('/reg_req', methods=['GET'])
def reg_req():
    livros = Livro.query.all()
    socios = Socio.query.all()
    return render_template('reg_req.html', livros=livros, socios=socios)


@app.route('/reg_req2', methods=['POST'])
def reg_req2():
    ISBN_r = int(request.form.get('isbns', ''))
    cc = int(request.form.get('ccs', ''))
    data_req = request.form.get('dt_req', '')
    data_entr = request.form.get('dt_ent', '')

    #validar, so socio ativo pode requisitar
    socio1 = db.session.query(Socio.ativo).filter_by(cc=cc).first()
    #validar sse o livro estiver livre
    livro1 = db.session.query(Livro.requisitado).filter_by(ISBN=ISBN_r).first()

    if socio1.ativo == "N":
        return render_template('invalido.html', cc=cc)

    if livro1.requisitado == "S":
        return render_template('invalido_livro.html', ISBN=ISBN_r)

    req = Requisito(ISBN_req=ISBN_r, cc_req=cc, data_req=data_req, data_entr=data_entr, completo='N')

    # alterar 'requisitado' do livro para 'S'
    db.session.query(Livro).filter(Livro.ISBN == ISBN_r).update({'requisitado': 'S'})

    db.session.add(req)
    db.session.commit()

    return render_template('sucesso.html')


@app.route('/compl_req', methods=['GET'])
def compl_req():
    reqs = Requisito.query.all()
    livros = db.session.query(Livro).filter_by(requisitado='S').all()
    return render_template('compl_req.html', reqs=reqs, livros=livros)


@app.route('/compl_req2', methods=['POST'])
def compl_req2():
    ISBN = request.form.get('isbns', '')
    data_entr = request.form.get('dt_ent', '')

    # alterar 'requisitado' do livro para 'N'
    db.session.query(Livro).filter(Livro.ISBN == ISBN).update({'requisitado': 'N'})
    # alterar requisito para completo S
    db.session.query(Requisito).filter(Requisito.ISBN_req == ISBN).update({'completo': 'S'})
    # update a data de entrega
    db.session.query(Requisito).filter(Requisito.ISBN_req == ISBN).update({'data_entr': data_entr})

    db.session.commit()

    return render_template('sucesso.html')


@app.route('/ver_req', methods=['GET'])
def ver_req():
    reqs = Requisito.query.all()
    return render_template('ver_req.html', reqs=reqs)


#Livro
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

    livro = Livro(ISBN=ISBN, titulo=tit, autor=autor, editora=editora, ano=ano, requisitado='N')

    db.session.add(livro)
    db.session.commit()

    return render_template('sucesso.html')


@app.route('/ver_livros', methods=['GET'])
def ver_livros():
    livros = Livro.query.all()
    return render_template('ver_livros.html', livros=livros)


#Socio
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


@app.route('/ver_soc', methods=['GET'])
def ver_soc():
    socios = Socio.query.all()
    return render_template('ver_soc.html', socios=socios)


@app.route('/altera_soc', methods=['POST'])
def altera_soc():
    cc = request.form.get('ccs', '')
    ativo = request.form.get('status', '')
    db.session.query(Socio).filter(Socio.cc == cc).update({'ativo': ativo})
    db.session.commit()
    return render_template('sucesso.html')


@app.route('/del_soc', methods=['GET'])
def del_soc():
    socios = Socio.query.all()
    return render_template('del_soc.html', socios=socios)


@app.route('/del_soc2', methods=['POST'])
def del_soc2():
    cc = request.form.get('ccs', '')
    Socio.query.filter_by(cc=cc).delete()
    db.session.commit()
    return render_template('sucesso.html')



###########################

port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    import  Database.Tables.Livro
    import  Database.Tables.Socio
    import  Database.Tables.Campanha
    import  Database.Tables.Requisito
    import  Database.Tables.Socio_Camp

    campanha1 = Campanha(nome_camp='Literatura Espanhola')
    campanha2 = Campanha(nome_camp='Literatura Lusófona')
    campanha3 = Campanha(nome_camp='Por todo o mundo...')
    campanha4 = Campanha(nome_camp='Literatura Estrangeira')
    db.session.add(campanha1)
    db.session.add(campanha2)
    db.session.add(campanha3)
    db.session.add(campanha4)

    livro1 = Livro(ISBN=9789720033109, titulo='O Retrato de Dorian Gray', autor='Oscar Wilde', editora='Porto Editora', ano=2020, requisitado='N')
    livro2 = Livro(ISBN=9789896445409, titulo='Sentir & Saber', autor='António Damásio', editora='Temas e Debates,', ano=2020, requisitado='N')
    livro3 = Livro(ISBN=9789896232245, titulo='Pequena Escola do Pensamento Filosófico', autor='Karl Jaspers ', editora='Cavalo de Ferro', ano=2016, requisitado='N')
    livro4 = Livro(ISBN=9781788162609, titulo='Lives Of The Stoics', autor='Stephen Hanselman e Ryan Holiday ', editora='Profile Books Ltd', ano=2020, requisitado='N')
    db.session.add(livro1)
    db.session.add(livro2)
    db.session.add(livro3)
    db.session.add(livro4)

    socio = Socio(cc=cc, nome_soc=nome_soc, email=email, data_n=data_n, morada=morada, ano_inscri=ano_inscri, ativo=ativo)
    socio = Socio(cc=cc, nome_soc=nome_soc, email=email, data_n=data_n, morada=morada, ano_inscri=ano_inscri, ativo=ativo)
    socio = Socio(cc=cc, nome_soc=nome_soc, email=email, data_n=data_n, morada=morada, ano_inscri=ano_inscri, ativo=ativo)
    socio = Socio(cc=cc, nome_soc=nome_soc, email=email, data_n=data_n, morada=morada, ano_inscri=ano_inscri, ativo=ativo)
    db.session.add(socio1)
    db.session.add(socio2)
    db.session.add(socio3)
    db.session.add(socio4)

    db.session.commit()
    db.create_all()
    app.run(host='0.0.0.0', port=port)