from flask import Flask, render_template, request
from google_sheet_api import google_sheet_api


flaskAppInstance = Flask(__name__)


@flaskAppInstance.route('/')
def hoome_page():
    return render_template("home.html")

@flaskAppInstance.route('/transform_spreadsheet', methods=["POST"])
def transform_spreadsheet():
    spreadsheet_id = request.form["spreadsheet_id"]
    sheet_name = request.form["sheet_name"]
    cell_range = sheet_name + "!A1:B"
    error = False
    try:
        sheet_data = google_sheet_api.get_rows_in_spreadsheet(spreadsheet_id, cell_range)
        text = "Spreadsheet Found and Transformed! Saved Intermediate File."
    except:
        text = "Some Error Occured"
        error = True
    print(text)
    return render_template("transform_file.html", text=text, error=error)

@flaskAppInstance.route('/validate')
def validate():
    return "<h2>Validate Sheet Records</h2>"

flaskAppInstance.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
    