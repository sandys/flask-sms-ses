import flask
from pprint import pprint
from time import sleep
from flask import Flask
from flask import Flask, render_template, request, flash
from forms import ContactForm,SMSForm
import boto.ses
import requests
from jinja2 import Template
from jinja2 import Environment, FileSystemLoader
from string import Template as String_Template
import re

# use as 'REDCARPET_SETTINGS=/path/to/settings.cfg python routes.py'
env = Environment(loader=FileSystemLoader('email_templates'))
contact_template = env.get_template('contact.html')
SMS_MESSAGE_DICT = {}
SMS_MESSAGE_DICT["WELCOME_MSG"] = String_Template("Congrats! You have now $points pts @ $merchant_name. Update email at www.redcarpetup.com and get free bonus pts! Optout: SMS STOP to +919871079907")
SMS_MESSAGE_DICT["REGISTER"] = String_Template("Welcome! You have $points pts on $customer_action @ $merchant_name. $call_to_action at $url_link & get $bonus_offer")

app = Flask(__name__)
app.config.from_envvar('REDCARPET_SETTINGS')
conn = boto.ses.connect_to_region('us-east-1',aws_access_key_id=app.config['AWS_ACCESS_KEY'],aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'])

app.secret_key = 'development key'


@app.route("/")
def hello():
    return "Hello World!"
import json


def get_sms_status(status_id):
  return requests.get(app.config['SINFINI_STATUS_URL'], params = {'workingkey':app.config['SINFINI_KEY'], "messageid":status_id}).text

@app.route('/sms', methods=['POST'])
def sms():
   form = SMSForm(csrf_enabled=False)
   if request.method == 'POST':
    if form.validate() == False:
      print form.errors
      return "Validation failed", 500
    else:
      sms_result = requests.get(app.config['SINFINI_API_URL'],params={'workingkey':app.config['SINFINI_KEY'], 'sender':app.config['SINFINI_SENDER_ID'],'to':form.sms_to.data,
                                                         'message':SMS_MESSAGE_DICT[form.sms_type.data].substitute(points=form.sms_points.data, merchant_name=form.sms_merchant_name.data, customer_action=form.sms_action.data, call_to_action=form.sms_call_action.data, url_link=form.sms_url.data, bonus_offer=form.sms_bonus.data)})

      #pprint (re.search(' ID=(.*)',sms_result.text).group(1))
      ID = re.search(' ID=(.*)',sms_result.text).group(1)
      sleep(5)
      return "Contact API success! SMS API response = " + get_sms_status(ID) ,200
 #&to="+"#{receiver_number}"+&message=


user_data = {'mobile':u'+917534865000',
             'total_points':10,
             'merchant_id':'Wokstar'}

def sendsms(to):
        SMSDATA = {'sms_to':to,
                   'customer_action':'Registration',
                   'call_to_action':'Update profile',
                   'url_link':'www.redcarpetup.com/profile',
                   'bonus_offer':'Free Drink',
                   'sms_type':'REGISTER',
                   'sms_points':'10',
                   'sms_merchant_name':'dfdfd'}
        print SMSDATA
        SMSFORM = type('sms',(object,),SMSDATA)
        smsresult = None
        smsresult = sms(SMSFORM)
        print "Sending SMS:",smsresult



@app.route('/email', methods=['POST'])
def email():
  form = ContactForm(csrf_enabled=False)

  if request.method == 'POST':
    if form.validate() == False:
      #return render_template('contact.html', form=form)
      print form.errors
      return "Validation failed", 500
    else:
      #mail.send(msg)
      ses_result = conn.send_email(app.config['SES_FROM_EMAIL'],form.subject.data,contact_template.render(foo=form.message.data),
              [form.email.data],format='html')

      return "Contact API success! AWS response = " + str(ses_result),200

  #elif request.method == 'GET':
  #  return render_template('contact.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

'''
from jinja2 import Template
Template("<h1>{{ foo }}</h1>").render(foo="sandeep")


conn = boto.ses.connect_to_region('us-east-1',aws_access_key_id='',aws_secret_access_key='')
def send_email_via_smtp(addresses, subject, text, html=None, attachment=None, from_name=None, from_address=None, **kwargs):
conn.send_email('sss@redcls.com','hi',Template("<html><body><h1>{{ foo }}</h1></body></html>").render(foo="sdeep"),['sss@reetup.com'],format='html')
    """
Send email via SMTP
"""
    server = webapi.config.get('smtp_server')
    port = webapi.config.get('smtp_port', 0)
    username = webapi.config.get('smtp_username')
    password = webapi.config.get('smtp_password')
    debug_level = webapi.config.get('smtp_debuglevel', None)
    starttls = webapi.config.get('smtp_starttls', False)

    import smtplib
    smtpserver = smtplib.SMTP(server, port)

    if debug_level:
        smtpserver.set_debuglevel(debug_level)

    if starttls:
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()

    if username and password:
        smtpserver.login(username, password)

    if html and text:
        message = MIMEMultipart('alternative')
        message.attach(MIMEText(html, 'html'))
        message.attach(MIMEText(text, 'plain'))
    elif html:
        message = MIMEText(html, 'html')
    else:
        message = MIMEText(text, 'plain')

    if attachment:
        tmpmessage = message
        message = MIMEMultipart()
        message.attach(tmpmessage)
        message.attach(MIMEText("\n\n", 'plain')) # helps to space the attachment from the body of the message
        log.info("--> adding attachment")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        message.attach(part)

    sender = from_name + "<" + from_address + ">"
    cc = listify(kwargs.get('cc', []))
    bcc = listify(kwargs.get('bcc', []))

    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ", ".join(addresses)
    message['Cc'] = ','.join(cc)
    message['Bcc'] = ','.join(bcc)

    smtpserver.sendmail(sender, addresses, message.as_string())
    smtpserver.quit()

def send_email_via_ses(addresses, subject, text, html=None, attachment=None, from_name=None, from_address=None, **kwargs):
    """
BCC is in kwargs
If SES has any error, the request will be passed back to the caller and domino down to SMTP
"""
    import boto.ses
    try:
        sesConn = boto.ses.SESConnection( aws_access_key_id = webapi.config.get('aws_access_key_id'),
                                      aws_secret_access_key = webapi.config.get('aws_secret_access_key'))
    except Exception, e:
        raise

    cc = listify(kwargs.get('cc', []))
    bcc = listify(kwargs.get('bcc', []))
    sender = from_name + "<" + from_address + ">"

    # First send emails without attachments and not multipart
    if (text and not html and not attachment) or \
       (html and not text and not attachment):
        return sesConn.send_email(sender, subject,
                                   text or html,
                                   addresses, cc, bcc,
                                   format='text' if text else 'html')
    else:
        if not attachment:
            message = MIMEMultipart('alternative')

            message['Subject'] = subject
            message['From'] = sender
            if isinstance(addresses, (list, tuple)):
                message['To'] = ','.join(addresses)
            else:
                message['To'] = addresses
            message['Cc'] = ','.join(cc)
            message['Bcc'] = ','.join(bcc)

            message.attach(MIMEText(text, 'plain'))
            message.attach(MIMEText(html, 'html'))
        else:
            # This raise should fall back into SMTP
            raise NotImplementedError, 'SES does not currently allow ' + \
                                       'messages with attachments.'

    # send_raw does not seem to support bcc or cc,
    # So let's force all our emails to go out as HTML
    return sesConn.send_email(sender, subject,
                              text or html,
                              addresses, cc, bcc,
                              format='html')

    # TODO: Fix the send_raw_email() so it support bcc and cc correctly!
    # return sesConn.send_raw_email(sender, message.as_string(), destinations=addresses)
'''
