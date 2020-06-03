"""
Contains all the forms required to obtain data from user.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class RepairsForm(FlaskForm):
    engineerName = SelectField(
        u'Select engineer:',
        choices = [('mWoods','Micheal Woods'),('jPonting','Jordan Ponting' ), ( 'pAdams','Paul Adams'), ('pCooper','Peter Cooper'), ('jStocks','John Stocks')], default='mWoods'
        
    )
    submit = SubmitField("Submit")