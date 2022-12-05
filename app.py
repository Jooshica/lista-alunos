from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route("/")
def index():
    tasks = []
    with open('alunos.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=",")
        first_line = True
        for row in data:
            if not first_line:
                tasks.append({
                    "nome": row[0],
                    "ano": row[1],
                    "situation": row[2],
                })
            else:
                first_line = False
    return render_template("home.html",tasks=tasks)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect(url_for('index'))

    elif request.method == 'POST':
        userdata = dict(request.form)
        nome = userdata["nome"]
        ano = userdata["ano"]
        situation = userdata["situation"]
        if len(nome) > 2 and len(situation) > 2 and int(ano) > 0:
            with open('alunos.csv', mode='a') as csv_file:
                data = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                data.writerow([nome, ano, situation])
        else:
            return redirect(url_for('index'))
        return redirect(url_for('index'))

@app.route("/delete", methods=['POST', 'GET'])
def delete():
    tasks = []
    if request.method == 'GET':
        return redirect(url_for('index'))

    elif request.method == 'POST':
        data = request.form["data"]
        with open('alunos.csv', 'rt') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                tasks.append(row)
                for field in row:
                    if field.lower() == data.lower():
                        tasks.remove(row)
        with open('alunos.csv', 'wt') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(tasks)
        return redirect(url_for('index'))

@app.route('/busca', methods=['POST'])
def busca():
    tasks = []
    with open('alunos.csv', 'rt') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            tasks.append(row)

    estudantes = []
    busca = request.form['busca']
    if busca > '':
        for estudante in tasks:
            if busca.lower() == estudante[0].lower():
                estudantes.append(estudante)
        
        return render_template('busca.html', estudantes=estudantes)

app.run(debug=True)