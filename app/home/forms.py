from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label="username",
        validators=[
            DataRequired("please input your username！")
        ],
        description="username",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "pls input your username here！"
        }
    )

    pwd = PasswordField(
        label="password",
        validators=[
            DataRequired("please input your password！")
        ],
        description="password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "pls input your password！"
        }
    )
    repwd = PasswordField(
        label="confirm password",
        validators=[
            DataRequired("pls input your password！"),
            EqualTo('pwd', message="password are different！")
        ],
        description="pls confirm your password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "pls input your password again！"
        }
    )

    submit = SubmitField(
        label="submit register",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError("username is already exist！")


class LoginForm(FlaskForm):
    name = StringField(
        label="username",
        validators=[
            DataRequired("pls input your username！")
        ],
        description="username",
        render_kw={

            "class": "form-control input-lg",
            "placeholder": "pls input your username at here！"
        }
    )

    pwd = PasswordField(
        label="password",
        validators=[
            DataRequired("pls input your password！")
        ],
        description="password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "pls input your password here！"
        }
    )

    submit = SubmitField(
        label="login",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

