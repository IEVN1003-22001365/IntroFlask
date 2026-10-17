import math
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def index():
    titulo="Pagina de inicio"
    listado = ['Python', 'Flask', 'Jinja2', 'HTML', 'CSS']
    return render_template("index.html",titulo=titulo,listado=listado)

@app.route("/operabas", methods=["GET", "POST"])
def operabas():
    n1 = 0
    n2 = 0
    res = 0
    operacion = ''

    if request.method == 'POST':
        n1 = float(request.form.get('n1'))
        n2 = float(request.form.get('n2'))
        operacion = request.form.get('operacion')

        if operacion == 'sumar':
            res = n1 + n2
        elif operacion == 'restar':
            res = n1 - n2
        elif operacion == 'multiplicar':
            res = n1 * n2

    return render_template('operabas.html', n1=n1, n2=n2, res=res, operacion=operacion)

@app.route("/distancia", methods=["GET", "POST"])
def distancia():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    resultado = None

    if request.method == 'POST':
        x1 = float(request.form.get('x1'))
        y1 = float(request.form.get('y1'))
        x2 = float(request.form.get('x2'))
        y2 = float(request.form.get('y2'))
        dif_x = x2 - x1
        dif_y = y2 - y1

        resultado = math.sqrt((dif_x * dif_x) + (dif_y * dif_y))
    return render_template('distancia.html', x1=x1, y1=y1, x2=x2, y2=y2, resultado=resultado)

@app.route("/hola")
def hola():
    return "<h1> Hola PWA - IEVN1003 </h1>"

@app.route("/user/<string:nom>")
def user(nom):
    return "<h1> Hola User: {} </h1>".format(nom)

@app.route("/numero/<int:n>")
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def username(id,username):
    return "ID: {} nombre: {}".format(id,username)

@app.route("/suma/<float:n1>/<float:n2>")
def func(n1,n2):
    return "La suma es: {}".format(n1+n2)

if __name__=="__main__":
    app.run(debug=True)