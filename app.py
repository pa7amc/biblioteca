from flask import Flask, render_template
import os
import sqlalchemy

app = Flask(__name__)


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
    app.run(host='0.0.0.0', port=port)