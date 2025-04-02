import pymysql.cursors
from flask import Flask, render_template, redirect, url_for, request, session

conn = pymysql.connect(host='172.16.12.54', user='ospite', password='ospite', database='db5CI')
cursore = conn.cursor()

app = Flask(__name__)

app.secret_key = 'ProvolaCiao'

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
    queryMedie = 'SELECT cognome, nome, AVG(voto) AS media FROM alunni, verifiche WHERE alunni.matricola = verifiche.studente GROUP BY studente'
    cursore.execute(queryMedie)
    risultatoMedie = cursore.fetchall()
    # print(risultatoMedie)
    return render_template("medie.html", medie=risultatoMedie, campi= cursore.description)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nuovoUser = request.form['username']
        nuovaPass = request.form['password']
        matricola = request.form['matricola']

        queryControllo = "SELECT * FROM utenti WHERE username = %s;"
        cursore.execute(queryControllo, (nuovoUser,))
        risultatiControllo = cursore.fetchall()

        if risultatiControllo:
            print("Utente già registrato.")
            return redirect(url_for('register'))

        queryControlloMatr = "SELECT matricola FROM alunni WHERE matricola = %s;"
        cursore.execute(queryControlloMatr, (matricola,))
        
        if not cursore.fetchall():
            print("La matricola non esiste!")
            return redirect(url_for('register'))

        queryInserimento = """INSERT INTO utenti VALUES (%s, %s, %s)"""
        cursore.execute(queryInserimento, (nuovoUser, nuovaPass, matricola))
        conn.commit()

        return redirect(url_for('login'))

    return render_template("register.html")

app.run(debug=True)