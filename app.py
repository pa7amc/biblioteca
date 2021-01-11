from flask import Flask, render_template, request
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Livro(db.Model):
    ISBN = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    autor = db.Column(db.String(70))
    editora = db.Column(db.String(70))
    ano = db.Column(db.Integer)
    #date = db.Column(db.DateTime, default=datetime.now)
    estado = db.Column(db.Integer)




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

    livro = Livro(ISBN=ISBN, titulo=tit, autor=autor, editora=editora, ano=ano, estado=0)

    db.session.add(livro)
    db.session.commit()

    return render_template('sucesso.html')



@app.route('/reg_req', methods=['GET'])
def reg_req():
    return render_template('reg_req.html')


@app.route('/reg_soc', methods=['GET'])
def reg_soc():
    return render_template('reg_soc.html')


@app.route('/ver_req', methods=['GET'])
def ver_req():
    return render_template('ver_req.html')


@app.route('/ver_soc', methods=['GET'])
def ver_soc():
    return render_template('ver_soc.html')







port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=port)