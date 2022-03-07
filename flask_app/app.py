from flask import Flask, render_template, request
from google_sheet_api import google_sheet_api
from util import functions
import datetime


flaskAppInstance = Flask(__name__)


@flaskAppInstance.route('/')
def home_page():
    return render_template("home.html")


@flaskAppInstance.route('/transform_spreadsheet', methods=["POST"])
def transform_spreadsheet():
    spreadsheet_id = request.form["spreadsheet_id"]
    sheet_name = request.form["sheet_name"]
    cell_range = sheet_name + "!A1:B"

    new_spreadsheet_id = request.form["new_spreadsheet_id"]
    new_sheet_name = request.form["new_sheet_name"]
    new_cell_range = new_sheet_name + "!A1:B"
    value_input_operation = "USER_ENTERED"
    error = False
    new_sheet_id = None
    try:
        sheet_data = google_sheet_api.get_rows_in_spreadsheet(spreadsheet_id, cell_range)
        transformed_data = functions.get_translated_rows(sheet_data)
        result = google_sheet_api.update_spreadsheet(new_spreadsheet_id, transformed_data, new_cell_range,
                                                     value_input_operation)
        #print(result)
        text = "Spreadsheet Found and Transformed! Saved Transformed Data To File."
        new_sheet_id = new_spreadsheet_id
    except Exception:
        text = "Some Error Occurred"
        error = True
    return render_template("transform_file.html", text=text, error=error, new_sheet_id=new_sheet_id,
                           new_sheet_name=new_sheet_name)

@flaskAppInstance.route('/manual_validation', methods=["POST"])
def fetch_spreadsheet():
    global count
    spreadsheet_id = request.form["new_spreadsheet_id"]
    sheet_name = request.form["new_sheet_name"]
    next_record = int(request.form["next_record"])
    current_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    if next_record > 1:
        row_json = dict()
        initial_english = request.form["initial_english"]
        initial_hindi = request.form["initial_hindi"]
        actual_hindi = request.form["actual_hindi"]
        cell_range = request.form["cell_range"]
        start = request.form["start"]
        row_json["Initial_English"] = initial_english
        row_json["Initial_Hindi"] = initial_hindi
        row_json["Actual_Hindi"] = actual_hindi
        row_json["Start"] = start
        row_json["End"] = current_time
        value_input_operation = "USER_ENTERED"
        row_list = functions.get_row_json_to_list(row_json)
        result = google_sheet_api.update_spreadsheet(spreadsheet_id, row_list, cell_range,
                                                     value_input_operation)
        print(result)

    elif next_record == 1:
        row_list = [["Initial_English", "Initial_Hindi", "Actual_Hindi", "Start", "End"]]
        value_input_operation = "USER_ENTERED"
        cell_range = sheet_name + "!A" + str(next_record) + ":E" + str(next_record)
        result = google_sheet_api.update_spreadsheet(spreadsheet_id, row_list, cell_range,
                                                     value_input_operation)
        print(result)

    next_record += 1
    cell_range = sheet_name + "!A" + str(next_record) + ":E" + str(next_record)
    print(cell_range)
    next_row = google_sheet_api.get_rows_in_spreadsheet(spreadsheet_id, cell_range)
    if len(next_row) > 0:
        next_row_json = functions.transform_row_list_to_json(next_row)
        records_present = True
        text = "Manual Validation Screen"
    else:
        text = "Validation Completed !!"
        records_present = False
        next_row_json = ['No new Rows']
    return render_template("manual_validation.html", text=text, row=next_row_json[0], records_present=records_present,
                           spreadsheet_id=spreadsheet_id, sheet_name=sheet_name, cell_range=cell_range,
                           next_record=next_record, start=current_time)


flaskAppInstance.run(host="localhost", port=5000, debug=True, use_reloader=True)
