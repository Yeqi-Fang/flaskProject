from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError


class NameForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    email = StringField('Enter our email.', validators=[DataRequired(), Email()])
    age = IntegerField('How old are your?', validators=[DataRequired(), NumberRange(min=3, max=100)])
    sex = SelectField('Sex', choices=[('男', '男'), ('女', '女'), ('', '保密')])
    submit = SubmitField('submit')

    def validate_name(self, name):
        from app import Role
        role = Role.query.filter_by(name=name.data).first()
        if role:
            raise ValidationError('姓名重复')

    def validate_email(self, email):
        from app import Role
        role = Role.query.filter_by(email=email.data).first()
        if role:
            raise ValidationError('邮箱重复')

