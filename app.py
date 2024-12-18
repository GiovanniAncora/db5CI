import pymysql.cursors
from flask import Flask, render_template

conn = pymysql.connect(host='172.16.12.54', user='ospite', password='ospite', database='db5CI')
cursore = conn.cursor()
query = 'SELECT * FROM alunni'
cursore.execute(query)

risultato = cursore.fetchall()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', alunni= risultato, campi= cursore.description)

@app.route('/<studente>')
def voti(studente):
    queryVoti = 'SELECT * FROM verifiche WHERE studente = %s'
    cursore.execute(queryVoti, (studente,))
    risultatoVoti = cursore.fetchall()
    return render_template("voti.html", voti=risultatoVoti, campi= cursore.description)

app.run(debug=True)