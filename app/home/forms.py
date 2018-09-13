from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired



class SearchForm(FlaskForm):
    """
    Form for users to login
    """
    search_ = StringField('', validators=[DataRequired()],render_kw={"placeholder": "Search: News Letters, Announcements, Inventory, Reports"})
    