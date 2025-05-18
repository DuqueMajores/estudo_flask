from app import app, db
from flask import render_template, url_for, request, redirect
from app.models import Contato
from app.forms import ContatoForm

@app.route("/")
def homepage():
    context = {
        'usuario':'Moises',
        'idade':28
    }
    return render_template('index.html', context=context)

### Formulario Seguro

@app.route("/formulario", methods=['GET', 'POST'])
def formulario_form():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template('contato_form.html', context=context, form=form)


### Formato nao recomendado

@app.route("/formulario_old", methods=['GET', 'POST'])
def formulario_old():
    context = {}
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa')
        context.update({'pesquisa':pesquisa})
        print('GET', pesquisa)
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        
        contato = Contato(
            nome = nome,
            email = email,
            assunto = assunto,
            mensagem = mensagem
        )

        db.session.add(contato)
        db.session.commit()

    return render_template('contato_old.html', context=context)
