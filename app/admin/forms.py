from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, DateField, HiddenField,PasswordField,SelectField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange

from ..models import User



class BinForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    depth = IntegerField('Bin Depth', validators=[DataRequired(),NumberRange(message="Invalid depth for bin.",min=1,max=10)])
    multi = HiddenField('multi') 
    submit = SubmitField('ADD')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('ADD')


class WarehouseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    locations =  SelectField('Location', coerce=int)

    submit = SubmitField('ADD')


class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('ADD')

class ModuleForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('ADD')

class ViewForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    modules =  SelectField('Modules', coerce=int)
    submit = SubmitField('ADD')

class SectionForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    views =  SelectField('Views', coerce=int)
    submit = SubmitField('ADD')

# class FeatureForm(FlaskForm):
#     """
#     Form for admin to add or edit a department
#     """
#     name = StringField('Name', validators=[DataRequired()])
#     sections =  SelectField('Sections', coerce=int)
#     submit = SubmitField('ADD')

# class AccessForm(FlaskForm):
#     """
#     Form for admin to edit user access
#     """
#     roles =  SelectField('Roles', coerce=int)
#     modules =  SelectField('Modules', coerce=int)
#     # views =  SelectField('Views', coerce=int)
#     # sections =  SelectField('Sections', coerce=int)
#     # stage =  HiddenField('Stage', validators=[DataRequired()])
#     # permission = SelectField('Access Level', coerce=int,choices=[(1,'Read'),(2,'Write'),(3,'Read / Write'),(4,'Execute'),(5,'All')])

#     submit = SubmitField('SAVE')


class RoleForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('ADD')


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male','Male'),('female','Female')])
    department = SelectField('Department', coerce=int)
    role = SelectField('Role', coerce=int)

    # password = PasswordField('Password', validators=[ DataRequired(), EqualTo('confirm_password')])
    # confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Save')
 
    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            if user.email != self.email.data:
                raise ValidationError('Username is already in use.')