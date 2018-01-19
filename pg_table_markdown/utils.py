from collections import defaultdict


def parse_schema_data(schema_data):
    output = defaultdict(list)
    for i in schema_data:
        table_name = i.pop('table_name')
        table_description = i.pop('table_description')
        output[" ".join([table_name,",",table_description])].append(i)
    return output
