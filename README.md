# Google_Sheet_Project

The objective of this project is to read a google sheet using google sheet API, apply a formula on the column in it and save entire data in a different file in google drive.
After this part is done, the next part is to display the rows one by one to the user. First column of a row contains an english sentence and the second column contains the hindi translation of the first column. The user is supposed to verify if the translation is correct, if not user should update the translation.
After this activity is performed by user the code should calculate the time taken by users to translate each row. This time taken by user and the correct translation should be updated back to the file.

## Prerequisites <br/>
### Creating a google sheet
To create a google sheet, you need to login to your google account and visit link - https://docs.google.com/spreadsheets <br/>
Here you can create a spreadsheet containing a column English Sentence.

### Create a service account on GCP to access spreadsheet with Google API
Follow these steps for the service account ceration
<ul>
  <li>You should have a GCP account for this project. Else you can create a free GCP account at - https://console.cloud.google.com/</li>
  <li>After the account is cerated login to the same link & create a new project.</li>
  <li>After creating project, go to APIs and services & hit on Enable APIs and Services. Select Google Drive API and Google Sheet API and enable them for this project.</li>
  <li>After that go to credentials tab in the left. In Service accounts sections, click on manage service accounts followed by create service account. Fill in the details and then you should have a service account.</li>
  <li>As a service account you'll get an email address. Click on that email and in keys section, click on ADD KEY button. Download that JSON and save to Google_Sheet_Project/flask_app/google_sheet_api/ directory as key.json</li>
</ul>

### Grant service account access to the spreadsheet
Open spreadsheet and click on share button on top right corner. Share the spreadsheet with the service account email. Give editor permission to it.

## Run the flask app 
For this project we can either setup a virtual python environment or go with the existing interpreter.
Just need to make sure the requirements.txt libraries are install. <br>
change directory to flask app where the requirements.txt and app.py reside<br>
cd flask_app <br><br>

Install requirements<br>
pip install -r requirements.txt<br><br>

Run the flask app<br>
python app.py

## Using the app
### Home Page
You need to provide the Original Spreadsheet id & sheet name as well as Target Spreadsheet Id and the Sheet Name. <br>
You can get the spreadsheet if in the URL of the spreadsheet.<br>
After the details are provided you need to submit that form.

### Transformation Page
On back of this page, the initial google English to Hindi transformation is applied and saved in B column.<br>
If any failures occure, warning button will show up on the screen asking you to go back to the homepage and fill the details again.<br>
If everything works fine, green button will appear asking you to go ahead.

### Manual Validation page
On this Page, you'll see the records one by one. User has to confirm if the google hindi translation is correct. If not, he can correct it in the Actual Translation field.<br>
After the last record in the sheet, the changes made will be saved to the Target spreadsheet.
Along with the actual hindi translation, the start and end time of each record will also be stored in the sheet.


