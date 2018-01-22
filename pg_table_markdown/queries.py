def build_schema_query(table_schema):
    schema_query = """
    SELECT c.table_name,
        trim((select pg_catalog.obj_description(oid) from pg_catalog.pg_class cl where cl.relname=c.table_name)) as table_description,
	    c.column_name,
        c.column_default, 
        c.is_nullable, 
        c.data_type, 
        c.character_maximum_length, 
        trim(pgd.description) as description
    FROM information_schema.columns c
    JOIN pg_catalog.pg_statio_all_tables as st ON (c.table_schema=st.schemaname and c.table_name=st.relname)
    LEFT JOIN pg_catalog.pg_description pgd on (pgd.objoid=st.relid AND pgd.objsubid=c.ordinal_position)
    WHERE       c.table_schema = '{0}'
    ORDER BY    c.table_name,
                c.ordinal_position
    """.format(table_schema)
    return schema_query
