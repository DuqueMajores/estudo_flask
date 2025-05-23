from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db, bcrypt
from app.models import Contato, User, Post, PostComentarios

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobreNome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirme_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            return ValidationError('Usuario ja cadastrado com esse e-mail!')
        
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome = self.nome.data,
            sobreNome = self.sobreNome.data,
            email = self.email.data,
            senha = senha
        )

        db.session.add(user)
        db.session.commit()
        return user
    
class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuario nao encontrado!')

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar', validators=[DataRequired()])

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()

class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        post = Post(
            mensagem = self.mensagem.data,
            user_id = user_id
        )

        db.session.add(post)
        db.session.commit()

class PostComentarioForm(FlaskForm):
    comentario = StringField('Comentario', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id, post_id):
        comentario = PostComentarios(
            comentario = self.comentario.data,
            user_id = user_id,
            post_id = post_id
        )

        db.session.add(comentario)
        db.session.commit()