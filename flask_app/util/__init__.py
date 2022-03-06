
class RequiredFunctions:
    def transform_row_list_to_json(self, row_list):
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

    def get_row_json_to_list(self, row_json):
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
