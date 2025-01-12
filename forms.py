from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ItemForm(FlaskForm):
    image_url = StringField('商品画像URL')
    name = StringField('商品名', validators=[DataRequired()])
    current_stock = IntegerField('現在の在庫数', validators=[NumberRange(min=0)])
    minimum_stock = IntegerField('必要な在庫数', validators=[NumberRange(min=0)])
    submit = SubmitField('保存')

class ConsumptionForm(FlaskForm):
    quantity = IntegerField('Quantity Used', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Log Consumption')
