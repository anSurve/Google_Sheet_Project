from flask import Flask, render_template, request
from google_sheet_api import google_sheet_api
import datetime


flaskAppInstance = Flask(__name__)

translated_row_list = list()
count = None
translated_row_json = list()


def transform_row_list_to_json(row_list):
    header = True
    row_out_list = list()
    for row in row_list:
        if header:
            key1 = row[0]
            key2 = row[1]
            key3 = "Actual_Hindi"
            key4 = "Start"
            key5 = "End"
            header = False
        else:
            row_dict = dict()
            row_dict[key1] = row[0]
            row_dict[key2] = row[1]
            row_dict[key3] = None
            row_dict[key4] = None
            row_dict[key5] = None
            row_out_list.append(row_dict)
    return row_out_list


def get_row_json_to_list(row_json):
    row_op_list = [["Initial_English", "Initial_Hindi", "Actual_Hindi", "Start", "End"]]
    for row in row_json:
        this_row_lst = list()
        this_row_lst.append(row["Initial_English"])
        this_row_lst.append(row["Initial_Hindi"])
        this_row_lst.append(row["Actual_Hindi"])
        this_row_lst.append(row["Start"])
        this_row_lst.append(row["End"])
        row_op_list.append(this_row_lst)
    return row_op_list


def get_translated_rows(rows_lst):
    counter = 1
    header = True
    for row in rows_lst:
        if header:
            header = False
            row.append("Initial_Hindi")
        else:
            row.append("=GOOGLETRANSLATE(A" + str(counter) + ",\"en\",\"hi\")")
        counter += 1
    return rows_lst


@flaskAppInstance.route('/')
def home_page():
    global translated_row_list
    global translated_row_json
    global count
    count = None
    translated_row_json.clear()
    translated_row_list.clear()
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
        transformed_data = get_translated_rows(sheet_data)
        result = google_sheet_api.update_spreadsheet(new_spreadsheet_id, transformed_data, new_cell_range,
                                                     value_input_operation)
        print(result)
        text = "Spreadsheet Found and Transformed! Saved Transformed Data To File."
        new_sheet_id = new_spreadsheet_id
    except Exception:
        text = "Some Error Occurred"
        error = True
    return render_template("transform_file.html", text=text, error=error, new_sheet_id=new_sheet_id)


@flaskAppInstance.route('/manual_validation', methods=["POST"])
def fetch_spreadsheet():
    global translated_row_list
    global count
    global translated_row_json
    spreadsheet_id = request.form["new_spreadsheet_id"]
    if count is None:
        cell_range = "Translation!A1:B"
        translated_row_list = google_sheet_api.get_rows_in_spreadsheet(spreadsheet_id, cell_range)
        count = 0
        translated_row_json = transform_row_list_to_json(translated_row_list)
    else:
        actual_hindi = request.form["actual_hindi"]
        translated_row_json[count]["Actual_Hindi"] = actual_hindi
        translated_row_json[count]["End"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(translated_row_json[count])
        count += 1
    row = None
    records_present = True
    if count < len(translated_row_json):
        row = translated_row_json[count]
        translated_row_json[count]["Start"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        print(translated_row_json[count])
        text = "Manual Validation Screen"
    else:
        records_present = False
        text = "Validation of all rows completed!"
        row_list = get_row_json_to_list(translated_row_json)
        cell_range = "Translation!A1:E"
        value_input_operation = "USER_ENTERED"
        result = google_sheet_api.update_spreadsheet(spreadsheet_id, row_list, cell_range,
                                                     value_input_operation)
        print(row_list)
    return render_template("manual_validation.html", text=text, row=row, records_present=records_present,
                           spreadsheet_id=spreadsheet_id)


flaskAppInstance.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
