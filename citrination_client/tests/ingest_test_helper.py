valid_general_csv_ingester_args = [
            {
                "name": "header_rows",
                "value": "3" # This should probably be registered in the ingester as a number, but right now it's a string
            },
            {
                "name": "column_one",
                "value": "col_title_1"
            },
            {
                "name": "column_two",
                "value": "col_title_2"
            }
        ]

general_csv_ingester_args_wrong_types = [
            {
                "name": "header_rows",
                "value": False
            },
            {
                "name": "column_one",
                "value": "valid_type"
            },
            {
                "name": "column_two",
                "value": 5
            }
        ]        