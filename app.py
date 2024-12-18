import pymysql.cursors
from flask import Flask, render_template

conn = pymysql.connect(host='172.16.12.54', user='ospite', password='ospite', database='db5CI')
cursore = conn.cursor()


app = Flask(__name__)

@app.route('/')
def index():
    query = 'SELECT * FROM alunni'
    cursore.execute(query)
    risultato = cursore.fetchall()
    return render_template('index.html', alunni= risultato, campi= cursore.description)

@app.route('/<studente>')
def voti(studente):
    queryVoti = 'SELECT * FROM verifiche WHERE studente = %s'
    cursore.execute(queryVoti, (studente,))
    risultatoVoti = cursore.fetchall()
    return render_template("voti.html", voti=risultatoVoti, campi= cursore.description)

@app.route('/medie')
def medie():
    queryMedie = 'SELECT nome, cognome, AVG(voto) AS media FROM alunni, verifiche WHERE alunni.matricola = verifiche.studente GROUP BY studente'
    cursore.execute(queryMedie)
    risultatoMedie = cursore.fetchall()
    # print(risultatoMedie)
    return render_template("medie.html", medie=risultatoMedie, campi= cursore.description)

app.run(debug=True)