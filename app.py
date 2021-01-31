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
    novo = db.Column(db.String(1))





@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

########### ####################      CAMPANHA
#Campanha
@app.route('/campanhas', methods=['GET'])
def campanhas():    
    campanhas = Campanha.query.all()
    return render_template('campanhas.html', campanhas=campanhas)


#Regista campanha
@app.route('/reg_camp', methods=['POST'])
def reg_camp():
    nome_campa = request.form.get('campa', '')
    campanha = Campanha(nome_camp=nome_campa)

    db.session.add(campanha)
    db.session.commit()
    return render_template('sucesso.html')

#Remover livro
@app.route('/del_camp', methods=['POST'])
def del_camp():
    campa = request.form.get('campa', '')
    Campanha.query.filter_by(id_camp=campa).delete()
    db.session.commit()
    return render_template('sucesso.html')



########### ####################      ADESAO
#Pagina adesao
@app.route('/socio_camp', methods=['GET'])
def socio_camp():    
    campanhas = Campanha.query.all()
    socios = Socio.query.all()
    sc = Socio_Camp.query.all()
    return render_template('socio_camp.html', campanhas=campanhas, sc=sc, socios=socios)


#Registar adesao
@app.route('/socio_camp2', methods=['POST'])
def socio_camp2():    
    id_campa = request.form.get('campa', '')
    cc_campa = request.form.get('ccs', '')
    novo = request.form.get('novo', '')

    adesao = db.session.query(Socio_Camp.cc_sc).filter_by(id_camp_sc=id_campa, cc_sc=cc_campa).first()

    if adesao != None:
        return render_template('invalido_adesao.html', cc_campa=cc_campa)
    

    sc = Socio_Camp(id_camp_sc=id_campa, cc_sc=cc_campa, novo=novo)

    db.session.add(sc)
    db.session.commit()
    return render_template('sucesso.html')


#Remover adesao
@app.route('/del_adesao', methods=['POST'])
def del_adesao():
    campa = request.form.get('campa', '')
    cc = request.form.get('ccs', '')

    adesao = db.session.query(Socio_Camp.id_sc).filter_by(id_camp_sc=campa, cc_sc=cc).first()
    #se o socio nao se encontrava no registo da adesao da campanha
    if  adesao is None:
        return render_template('invalido_rem_adesao.html', cc_campa=cc, id_camp_sc=campa)


    Socio_Camp.query.filter_by(id_camp_sc=campa, cc_sc=cc).delete()
    db.session.commit()
    return render_template('sucesso.html')



########### ####################      REQUISITO
#Requisito
@app.route('/reg_req', methods=['GET'])
def reg_req():
    livros = Livro.query.all()
    socios = Socio.query.all()
    return render_template('reg_req.html', livros=livros, socios=socios)


#Registar requisito
@app.route('/reg_req2', methods=['POST'])
def reg_req2():
    ISBN_r = int(request.form.get('isbns', ''))
    cc = int(request.form.get('ccs', ''))
    data_req = request.form.get('dt_req', '')
    data_entr = request.form.get('dt_ent', '')
    
    socio1 = db.session.query(Socio.ativo).filter_by(cc=cc).first()
    livro1 = db.session.query(Livro.requisitado).filter_by(ISBN=ISBN_r).first()

    #validar, so socio ativo pode requisitar
    if socio1.ativo == "N":
        return render_template('invalido.html', cc=cc)
    #validar sse o livro estiver livre
    if livro1.requisitado == "S":
        return render_template('invalido_livro.html', ISBN=ISBN_r)

    req = Requisito(ISBN_req=ISBN_r, cc_req=cc, data_req=data_req, data_entr=data_entr, completo='N')

    # alterar 'requisitado' do livro para 'S'
    db.session.query(Livro).filter(Livro.ISBN == ISBN_r).update({'requisitado': 'S'})

    db.session.add(req)
    db.session.commit()
    return render_template('sucesso.html')


#Pagina fechar requisito
@app.route('/compl_req', methods=['GET'])
def compl_req():
    reqs = Requisito.query.all()
    livros = db.session.query(Livro).filter_by(requisitado='S').all()
    return render_template('compl_req.html', reqs=reqs, livros=livros)


#Fechar requisito
@app.route('/compl_req2', methods=['POST'])
def compl_req2():
    ISBN = request.form.get('isbns', '')
    data_entr = request.form.get('dt_ent', '')

    # alterar 'requisitado' do livro para 'N'
    db.session.query(Livro).filter(Livro.ISBN == ISBN).update({'requisitado': 'N'})
    # alterar requisito para completo 'S'
    db.session.query(Requisito).filter(Requisito.ISBN_req == ISBN).update({'completo': 'S'})
    # update na data de entrega
    db.session.query(Requisito).filter(Requisito.ISBN_req == ISBN).update({'data_entr': data_entr})

    db.session.commit()
    return render_template('sucesso.html')

#Ver requisitos
@app.route('/ver_req', methods=['GET'])
def ver_req():
    reqs = Requisito.query.all()
    return render_template('ver_req.html', reqs=reqs)


########### ####################      LIVRO
#Livro
@app.route('/reg_livro', methods=['GET'])
def reg_livro():
    return render_template('reg_livro.html')


#Registo do livro
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


#Ver livros
@app.route('/ver_livros', methods=['GET'])
def ver_livros():
    livros = Livro.query.all()
    return render_template('ver_livros.html', livros=livros)


#Pagina remove livro
@app.route('/del_livro', methods=['GET'])
def del_livro():
    livros = Livro.query.all()
    return render_template('del_livro.html', livros=livros)


#Remover livro
@app.route('/del_livro2', methods=['POST'])
def del_livro2():
    isbn = request.form.get('isbns', '')
    livro1 = db.session.query(Livro.requisitado).filter_by(ISBN=isbn).first()

        #se o livro esta requisitado, nao se pode apagar
    if livro1.requisitado == "S":
            return render_template('invalido_livro.html', ISBN=isbn)

    Livro.query.filter_by(ISBN=isbn).delete()
    db.session.commit()
    return render_template('sucesso.html')



########### ####################      SOCIO
#Pagina registo Socio
@app.route('/reg_soc', methods=['GET'])
def reg_soc():
    return render_template('reg_soc.html')


#Registar socio
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


#Ver socios
@app.route('/ver_soc', methods=['GET'])
def ver_soc():
    socios = Socio.query.all()
    return render_template('ver_soc.html', socios=socios)


#Alterar estado do socio
@app.route('/altera_soc', methods=['POST'])
def altera_soc():
    cc = request.form.get('ccs', '')
    ativo = request.form.get('status', '')
    db.session.query(Socio).filter(Socio.cc == cc).update({'ativo': ativo})
    db.session.commit()
    return render_template('sucesso.html')


#Pagina remove socio
@app.route('/del_soc', methods=['GET'])
def del_soc():
    socios = Socio.query.all()
    return render_template('del_soc.html', socios=socios)


#Remover socio
@app.route('/del_soc2', methods=['POST'])
def del_soc2():
    cc = request.form.get('ccs', '')

    req_ativo = db.session.query(Requisito.id_req).filter_by(cc_req=cc, completo="N").first()

        #se o socio tiver requisitos por fechar
    if req_ativo != None:
            return render_template('invalido_rem_soc.html', cc=cc)


    Socio.query.filter_by(cc=cc).delete()
    db.session.commit()
    return render_template('sucesso.html')



###########################

port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=port)