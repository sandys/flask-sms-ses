from flask_wtf import Form
from wtforms import IntegerField,TextField,TextAreaField, SubmitField
from wtforms.validators import DataRequired,URL

class ContactForm(Form):
  name = TextField("Name", validators=[DataRequired()])
  email = TextField("Email", validators=[DataRequired()])
  subject = TextField("Subject", validators=[DataRequired()])
  message = TextAreaField("Message", validators=[DataRequired()])
  submit = SubmitField("Send")

class SMSForm(Form):
  sms_type = TextField("sms-type", validators=[DataRequired()])
  sms_to = IntegerField("sms-to", validators=[DataRequired()] )
  sms_merchant_name = TextField("sms-merchant-name")
  sms_points = IntegerField("sms-points")
  sms_action = TextField("sms-action")
  sms_call_action = TextField("sms-call-action")
  sms_url= TextField("sms-url" )
  sms_bonus= TextField("sms-bonus")

