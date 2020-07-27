from flask_wtf import FlaskForm
from wtforms import DecimalField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class OrderRequestForm(FlaskForm):
    amount = DecimalField(
        'Сумма оплаты',
        places=2, # be carefull with money rounding, it's a bit tricky way.
        validators=[DataRequired()],
    )
    currency = SelectField(
        'Валюта оплаты',
        choices=[
            ('EUR', 'EUR'),
            ('USD', 'USD'),
            ('RUB', 'RUB')]
    )
    item_description = TextAreaField(
        'Описание товара',
        validators=[
            DataRequired(),
            Length(max=250, message=('Your message is too long.'))]
    )
    submit = SubmitField('Оплатить')
