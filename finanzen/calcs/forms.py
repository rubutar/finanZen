from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, DateField, IntegerField
from wtforms.validators import DataRequired

class CalcForm(FlaskForm):
    # tick = StringField('Tick', validators=[DataRequired()])
    ticker = StringField('Ticker', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    purchase_price = DecimalField('Price per Share', validators=[DataRequired()])
    purchase_date = DateField('Date Purchased', validators=[DataRequired()])
    submit = SubmitField('Submit')