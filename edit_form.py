from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    rating = StringField('Your Rating  out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit')