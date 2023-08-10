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
    severity = 'BLUE'
    recommendation = 'Self guided support'
    data = request.get_json()
    admin_emails = [user['email'] for user in db.Users.find()]
    total_score = process_answer(data)
    if 3 <= total_score <= 4 :
        severity = 'GREEN'
        recommendation = 'counselling and self guided support'
    elif 5 >= total_score <= 6:
        severity = 'YELLOW'
        recommendation = 'specialized one on one counselling + self guided support in between sessions'
    elif 7 >= total_score <= 9:
        severity = 'ORANGE'
        recommendation = 'specialized one on one counselling with community care coordinator to explore nutrition and integrative medicine services'
    elif total_score >= 10:
        severity = 'RED'
        recommendation = 'specialized one on one counselling with brainspotting, prepare for EMDR, potential psychedelic assisted therapy. Should look at nutrition and integration medicine'
    data['recommendation'] = recommendation
    data['severity'] = severity
    data['score'] = total_score
    #data['severity_breakdown'] = breakdown
    db.Trauma.insert_one(data)
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
