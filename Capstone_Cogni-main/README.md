# Capstone_Cogni
Main files to keep in mind.
 - answers_config.yaml
 - app.py
 - env.example
 - requirements.txt
 - utils.py

**answers_config.yaml**  

This file consists of mapped answers of the questionares with the scores.Every response has a score provided in this file so mapping of each and every options with the score can be done here. Every entry is a key value pair so important keys and their values are described below:
- question_slug means the name or the identifier use to denote a question can be entered in this key.
- type means wat kind of questionare is it? single select and text are the widely used options.
- answer_scores means what weightage/score should be given to each option will be mentioned here.

**app.py**
This file consist of the mathematical model logics where the scores are bifurcated to 3 different clusters namely red,orange and green. All the three categories are alloted scores and based on the total score obtanied from each reponse it falls into any one of the category. Also, the mail trigerring logic is mentioned here.

**env.example**
All the environment variables necessary to make the app work is described here. 
MONGO_URI,MAIL_DEFAULT_SENDER,MAIL_SERVER,MAIL_USERNAME,MAIL_PASSWORD,GCLOUD_PROJECT are the required fields which needs to be filled.

**requirements.txt**
This file consist of all the required packages libraries used to make the app eun. Make sure you have all this things installed at your end individually or exporting the requirements.txt file via python.

**utils.py**
Database and mail settitngs can be found in this file. Other than that reading the answer config file can be seen here. And based on that teh severity score is logged.

**cognixrsummary.html**
This file contains the UI part displayed in the mail. Basically the template where the user sees the score in the email.

**FLow of the project**
- Github has the answer file named as answers_config.yaml where all the answers are logged with the desired scores for each response.
- The names given for each question_slug is used in the power automate software. Every question slug is mapped to the correct questions in power automate so that we get the proper response to that particular question.
- Automated flow is created in powerautmate which will trigger the given survey form and retrieve all the answers with the help of a HTTP POST method.
- All the answers are then stored into Mongo DB and the finally the score is sent to the user email mentioned in the questionare with few details of demographics etc.
