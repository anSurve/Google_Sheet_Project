
class RequiredFunctions:
    def transform_row_list_to_json(self, row_list):
        row_out_list = list()
        key1 = "Initial_English"
        key2 = "Initial_Hindi"
        key3 = "Actual_Hindi"
        key4 = "Start"
        key5 = "End"
        key6 = "Elapsed_Time"
        for row in row_list:
            row_dict = dict()
            row_dict[key1] = row[0]
            row_dict[key2] = row[1]
            row_dict[key3] = None
            row_dict[key4] = None
            row_dict[key5] = None
            row_dict[key6] = None
            row_out_list.append(row_dict)
        return row_out_list

    def get_row_json_to_list(self, row):
        this_row_lst = list()
        this_row_lst.append(row["Initial_English"])
        this_row_lst.append(row["Initial_Hindi"])
        this_row_lst.append(row["Actual_Hindi"])
        this_row_lst.append(row["Start"])
        this_row_lst.append(row["End"])
        this_row_lst.append(row["Elapsed_Time"])
        return [this_row_lst]

    def get_translated_rows(self, rows_lst):
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


functions = RequiredFunctions()
