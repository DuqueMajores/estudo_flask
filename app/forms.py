from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

from app import db
from app.models import Contato

class ContatoForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    assunto = StringField('assunto', validators=[DataRequired()])
    mensagem = StringField('mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('enviar', validators=[DataRequired()])

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()
