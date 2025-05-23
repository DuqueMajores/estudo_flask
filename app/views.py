from app import app, db
from flask import render_template, url_for, request, redirect
from flask_login import login_required
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Contato, Post
from app.forms import ContatoForm, UserForm, LoginForm, PostForm, PostComentarioForm

### Pagina Index
@app.route("/", methods=['GET', 'POST'])
def homepage():

    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        
    print(current_user.is_authenticated)

    context = {
        'usuario':'Moises',
        'idade':28
    }
    return render_template('index.html', context=context, form=form)

###Rota Cadastro de Usuario
@app.route("/cadastro/", methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    context = {}
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html',context=context, form=form)

###Logout 
@app.route("/sair/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

###Rota Post
@app.route("/post/novo/", methods=['GET', 'POST'])
@login_required
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('homepage'))
    return render_template('post_novo.html', form=form)

###Lista de Posts
@app.route("/post/lista/")
@login_required
def PostLista():
    posts = Post.query.all()
    return render_template('post_lista.html', posts=posts)

###Comentarios
@app.route("/post/<int:id>", methods=['GET', 'POST'])
@login_required
def PostDetalhe(id):
    post = Post.query.get(id)
    form = PostComentarioForm()
    if form.validate_on_submit():
        form.save(current_user.id, id)
        return redirect(url_for('PostDetalhe', id=id))
    return render_template('post.html', post=post, form=form)

### Formulario Seguro
@app.route("/formulario", methods=['GET', 'POST'])
@login_required
def formulario_form():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))

    return render_template('contato_form.html', context=context, form=form)

### Lista de Contatos
@app.route('/contato/lista')
@login_required
def contatoLista():

    if current_user.id == 1: return redirect(url_for('homepage'))

    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by('id')
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
    context = {'dados':dados.all()}
    pessoas = Contato.query.all()
    quantidade = len(pessoas)

    for linha in dados:
        print(linha.nome)

    return render_template('contato_lista.html', context=context, pessoas=pessoas, quantidade=quantidade)

### Rota Dinamica
@app.route('/contato/<int:id>/')
@login_required
def contato_detalhe(id):
    obj = Contato.query.get(id)
    return render_template('contato_detalhe.html', obj=obj)

### Formulario nao recomendado
@app.route("/formulario_old", methods=['GET', 'POST'])
@login_required
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
