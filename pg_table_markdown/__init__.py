import sys
import click
from pg_table_markdown.database import database_connection, UnableToConnectToDatabase
from pg_table_markdown.utils import parse_schema_data
from pg_table_markdown.queries import build_schema_query


SECTION_HEADING = '### {0} \n\n'
SECTION_TABLE_DESC = '{0} \n\n'
TABLE_HEADER = 'Column | Type | Default | Nullable \n'
TABLE_DIVIDER = '--- | --- | --- | --- \n'
TABLE_ROW = '{column_name} | {data_type} | {column_default} | {is_nullable} \n'
TABLE_ROW_WITH_MAXLENGTH = '{column_name} | {data_type}({character_maximum_length}) | {column_default} | {is_nullable} \n'

TABLE_HEADER_WITH_DESCRIPTION = 'Column | Type | Default | Nullable | Description \n'
TABLE_DIVIDER_WITH_DESCRIPTION = '--- | --- | --- | --- | --- \n'
TABLE_ROW_WITH_DESCRIPTION = '{column_name} | {data_type} | {column_default} | {is_nullable} | {description} \n'
TABLE_ROW_WITH_MAXLENGTH_WITH_DESCRIPTION = '{column_name} | {data_type}({character_maximum_length}) | {column_default} | {is_nullable} | {description} \n'


@click.command()
@click.option('--database_url', prompt=True, help='Database connection URL')
@click.option('--table_schema', default='public', help='Postgres table_schema, default is: public')
@click.option('--output_file', prompt=True, help='Path for generated markdown file')
@click.option('--max_length', is_flag=True, help='To display maximum length of character varying, default is: False')
@click.option('--description_text', is_flag=True, help='To display description for the column, default is: False')

def cli(database_url, table_schema, output_file, max_length, description_text):
    """
    Export Postgres table documentation to a markdown file
    """
    try:
        db = database_connection(database_url=database_url)
    except UnableToConnectToDatabase:
        click.echo("Unable to connect to database using 'database_url': {0}".format(database_url))
        sys.exit(1)

    cursor = db.cursor()
    cursor.execute(build_schema_query(table_schema=table_schema))
    results = cursor.fetchall()
    cursor.close()

    parsed = parse_schema_data(schema_data=results)
    
    if description_text:
            TABLE_HEADER = TABLE_HEADER_WITH_DESCRIPTION
            TABLE_DIVIDER = TABLE_DIVIDER_WITH_DESCRIPTION
            TABLE_ROW = TABLE_ROW_WITH_DESCRIPTION
            TABLE_ROW_WITH_MAXLENGTH = TABLE_ROW_WITH_MAXLENGTH_WITH_DESCRIPTION

    with open(output_file, 'w') as f:
        for table_name_desc in sorted(parsed.keys()):
            table_name,table_desc = table_name_desc.split("$")
            f.write(SECTION_HEADING.format(table_name))
            f.write(SECTION_TABLE_DESC.format(table_desc))
            f.write(TABLE_HEADER)
            f.write(TABLE_DIVIDER)
            for column in parsed[table_name_desc]:
                if max_length and column['character_maximum_length'] is not None:
                    f.write(TABLE_ROW_WITH_MAXLENGTH.format(**column))
                else:
                    f.write(TABLE_ROW.format(**column))
            f.write('\n')
