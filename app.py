from flask import Flask, render_template, request
import csv

app = Flask(__name__)

#tasks = [
    #{'name': 'Nome', 'ano': '8','situation':'Situação'}
#]

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

#@app.route('/')
#def home():
    #templates/home.html
    #return render_template('home.html', tasks=tasks)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return redirect(url_for('home'))

    elif request.method == "POST":
        userdata = dict(request.form)
        nome = userdata["nome"]
        ano = userdata["ano"]
        situation = userdata["situation"]
        with open('alunos.csv', mode='a') as csv_file:
            data = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data.writerow([nome, ano, situation])
        return "Valeu"

#@app.route('/create', methods={'POST'})
#def create():
    #name = request.form['name']
    #ano = request.form['ano']
    #situation = request.form['situation']
    #task = {'name': name, 'ano': ano, 'situation': situation}
    #tasks.append(task)
    #return render_template('home.html', tasks=tasks)

@app.route('/delete',methods=["POST"])
def delete_book():
    id = request.form.get('id')
    if id != None:
        with open('alunos.csv', 'rt') as f:
            alunes = list(csv.reader(f))
            for alune in alunes:
                if alune[0] == id:
                    alunes.remove(alune)
        with open('alunos.csv', 'wt',newline='') as f:
            write = csv.writer(f)
            write.writerows(alune)
        return redirect(url_for('adicionados'))
    else:
        print('id não pode ser nulo')
        return redirect(url_for('adicionados'))

app.run(debug=True)