from flask import Flask, render_template, request
from pymongo import MongoClient
from flask_mail import Mail, Message
from utils import MongoEncoder, DATABASE_URI, mail_settings
from utils import process_answer

client = MongoClient(DATABASE_URI)
db = client['Cogni4health']

app = Flask(__name__)
app.json_encoder = MongoEncoder
app.config.update(mail_settings)
mail = Mail(app)

@app.get('/')
def index():
    if (db.response.count_documents({}) > 0):
        sample_record = db.response.find_one({}, sort=[( '_id', -1 )])
        admin_emails = [user['email'] for user in db.Users.find()]
        msg = Message('Health and Wellness Survey: New Submission Receieved!', recipients=admin_emails)
        msg.body = render_template('cognixrsummary.html', **sample_record)
        msg.html = render_template('cognixrsummary.html', **sample_record)
        mail.send(msg)
        return render_template('cognixrsummary.html', **sample_record)
    else:
        return ('Test failed')
    

@app.post('/')
def get_form_submission():
    severity = 'GREEN'
    data = request.get_json()
    admin_emails = [user['email'] for user in db.Users.find()]
    total_score = process_answer(data)
    if total_score > 96:
        severity = 'RED'
    elif total_score > 48:
        severity = 'AMBER'
    data['severity'] = severity
    data['score'] = total_score
    #data['severity_breakdown'] = breakdown
    db.response.insert_one(data)
    msg = Message('Health and Wellness Survey: New Submission Receieved!', recipients=admin_emails)
    msg.body = render_template('cognixrsummary.html', **data)
    msg.html = render_template('cognixrsummary.html', **data)
    mail.send(msg)
    if data.get('Email') != None:
        msg.recipients = [data['Email']]
        mail.send(msg)
    return {'success': True, 'data': data}

if __name__ == '__main__':
	app.run(debug=True)
