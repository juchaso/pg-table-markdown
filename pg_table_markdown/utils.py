from collections import defaultdict


def parse_schema_data(schema_data):
    output = defaultdict(list)
    for i in schema_data:
        table_name = i.pop('table_name')
        table_description = i.pop('table_description')
        if table_description is None:
            table_description = 'None'
        output[" ".join([table_name,',',table_description])].append(i)
    return output
