from flask import Flask, request, render_template, jsonify
from postdb import search_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def results():
    tgtword = request.form.get('input')
    results = search_data(tgtword)
    return render_template("results.html", tgtword=tgtword, results=results)

if __name__ == '__main__':
    app.run(port=8000, debug=True)



