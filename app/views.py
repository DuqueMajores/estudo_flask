from app import app
from flask import render_template, url_for, request

@app.route("/")
def homepage():
    context = {
        'usuario':'Moises',
        'idade':28
    }
    return render_template('index.html', context=context)

@app.route("/formulario")
def formulario():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa':pesquisa})
    return render_template('contato.html', context=context)
