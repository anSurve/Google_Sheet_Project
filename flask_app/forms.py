from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class SpreadSheetForm(FlaskForm):
    spreadsheet_id = StringField(label='Spreadsheet Id :')
    sheet_name = StringField(label='Sheet Name :')
    submit = SubmitField(label='Submit')