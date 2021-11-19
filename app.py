from flask import Flask, render_template, url_for, flash, redirect, request
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError 
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import json
import email_validator

SECRET_KEY = "vladsecretkey"
WTF_CSRF_ENABLED = True

app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisasecret!"
#app.config.from_object("config")
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class RegistrationForm(FlaskForm):
    login = StringField("Логін (адреса електронної пошти)*", validators=[Email(message="Неправильно введена електронна пошта"), DataRequired(message="Це поле має бути обов'язкове")])
    password = PasswordField("Пароль *", validators=[
                                    Length(min=6, message="Пароль мусить бути не менше 6 символів"), 
                                    DataRequired(message="Це поле має бути обов'язкове")
                                ])
    confirm_password = PasswordField("Підтвердження паролю", validators=[
                                    DataRequired(message="Це поле має бути обов'язкове"),
                                    EqualTo("password")])
    number = StringField("Номер *", validators=[
                                Regexp(r"^[0-9]{7}$", message="Поле повинно містити строго 7 цифр"),
                                DataRequired(message="Це поле має бути обов'язкове")])
    pin = StringField("Пін *", validators=[
                                Regexp(r"^[0-9]{4}$", message="Поле повинно містити строго 4 цифр"),
                                DataRequired(message="Це поле має бути обов'язкове")])
    year = SelectField("Рік *", choices=range(1980, 2022))
    
    diplom_serial = StringField("Серія")
    diplom_number = StringField("Номер *")
    submit = SubmitField("Зареєструвати")

def add_info(validate):
    dictionary = {}
    data = {
        validate.login.data: { "password" : validate.password.data, "number_e" : validate.number.data,
            "pin_e" : validate.pin.data,
            "year_of_receive": validate.year.data,
            "diplom_serial": validate.diplom_serial.data,
            "diplom_number" : validate.diplom_number.data
        }
    }
    try:
        with open("registers.json", "r") as file:
            dictionary = json.load(file)
            dictionary.update(data)

        with open("registers.json", "w", encoding="utf-8") as write_file:
            json.dump(dictionary, write_file, ensure_ascii = False, indent = 4)

    except FileNotFoundError or json.decoder.JSONDecodeError:
        with open("registers.json", "w", encoding="utf-8") as write_file:
            json.dump(data, write_file, ensure_ascii = False, indent = 4)

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = RegistrationForm()
    data = form.year.data
    if data is not None and int(data) < 2015:
        form.diplom_serial.validators = [Regexp(r"^[A-Z]{2}$", message="Серія диплому повинна складатись з двох латинських літер (до 2015 року) або з латинської літери та двох цифр(з 2015 року)!")]
        form.diplom_number.validators = [Regexp(r"^[0-9]{8}$", message="Номер диплому повинен складатись з 8 цифр (до 2015 року) або з 6 цифр (після 2015 року)!"), DataRequired(message="Це поле має бути обов'язкове")]
    else:
        form.diplom_serial.validators = [Regexp(r"^[A-Z]{1}[0-9]{2}$", message="Серія диплому повинна складатись з двох латинських літер (до 2015 року) або з латинської літери та двох цифр(з 2015 року)!")]
        form.diplom_number.validators = [Regexp(r"^[0-9]{6}$", message="Номер диплому повинен складатись з 8 цифр (до 2015 року) або з 6 цифр (після 2015 року)!"), DataRequired(message="Це поле має бути обов'язкове")]
    if form.validate_on_submit():
        flash('Дані занесені успішно!')
        add_info(form)
        return redirect(url_for('form'))
    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)