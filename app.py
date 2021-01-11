from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')







port = int(os.getenv("PORT", 5000))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)