from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

@app.route("/")
def index():
    with open('alunos.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=",")
        first_line = True
        tasks = []
        for row in data:
            if not first_line:
                tasks.append({
                    "nome": row[0],
                    "ano": row[1],
                    "situation": row[2]
                })
            else:
                first_line = False
    return render_template("home.html",tasks=tasks)

@app.route("/", methods=['GET', 'POST'])
def submit():
    tasks = []
    if request.method == 'GET':
        return redirect(url_for('index'))

    elif request.method == 'POST':
        userdata = dict(request.form)
        nome = userdata["nome"]
        ano = userdata["ano"]
        situation = userdata["situation"]
        with open('alunos.csv', mode='a') as csv_file:
            data = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data.writerow([nome, ano, situation])
        return redirect(url_for('index'))

@app.route("/", methods=['POST', 'GET'])
def delete():
    tasks = []
    if request.method == 'GET':
        return redirect(url_for('index'))

    elif request.method == 'POST':
        dados = request.form.get("data")
        with open('alunos.csv', 'rt') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                tasks.append(row)
                for field in row:
                    if field == dados:
                        tasks.remove(row)
        with open('alunos.csv', 'wt') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(tasks)
        return redirect(url_for('index'))

app.run(debug=True)