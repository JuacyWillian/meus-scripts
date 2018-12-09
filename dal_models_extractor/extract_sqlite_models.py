'''
Create the web2py model code needed to access your sqlite legacy db.
Usage:
    python extract_sqlite_models.py

Access your tables with:
    db(legacy_db.mytable.id>0).select()

extract_sqlite_models.py -- Copyright (C) Michele Comitini

This code is distributed with web2py.
The regexp code and the dictionary type map was extended from
extact_mysql_models.py that comes with web2py.
extact_mysql_models.py is Copyright (C) Falko Krause.

this code was modified and fixed for Juacy Willian in 12/2018
'''
import re
import sqlite3
import sys

header = '''
# coding: utf-8
""" Extract models from sqlite database

File Generated automatically by extract_sqlite_models.py



"""\n\n
'''

data_type_map = dict(
    varchar='string',
    int='integer',
    integer='integer',
    tinyint='integer',
    smallint='integer',
    mediumint='integer',
    bigint='integer',
    float='double',
    double='double',
    char='string',
    decimal='integer',
    date='date',
    time='time',
    timestamp='datetime',
    datetime='datetime',
    binary='blob',
    blob='blob',
    tinyblob='blob',
    mediumblob='blob',
    longblob='blob',
    text='text',
    tinytext='text',
    mediumtext='text',
    longtext='text',
    bit='boolean',
    nvarchar='text',
    numeric='decimal(30,15)',
    real='decimal(30,15)',
)


def get_foreign_keys(sql_lines):
    fks = dict()
    for line in sql_lines[1:-1]:
        if 'references' not in line.lower():
            continue
        hit = re.search(
            r'(\S+) .*? REFERENCES ((\S+) \((\S+)\))', line)
        if hit:
            fks[hit.group(1)] = hit.groups()[2:]

    return fks


def get_formated_sql(sql_):
    return sql_.replace('(', '(\n', 1) \
        .replace('"', '') \
        .replace(',', ',\n')


def sqlite(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    r = c.execute(
        r"select name,sql from sqlite_master where type='table' and not name like '\\_%' and not lower(name) like 'sqlite_%'")
    tables = r.fetchall()
    connection_string = "from pydal import DAL, Field\n\n\n"
    connection_string += "db = DAL('sqlite://%s')" % database_name
    legacy_db_table_web2py_code = []
    for table_name, sql_create_stmnt in tables:
        if table_name.startswith('_'):
            continue

        if 'CREATE' in sql_create_stmnt:  # check if the table exists
            sql_lines = get_formated_sql(sql_create_stmnt).split('\n')
            sql_lines = [x for x in sql_lines if not (
                    x.startswith('--') or x.startswith('/*')
            )]

            web2py_table_code = ''
            fields = []
            fks = get_foreign_keys(sql_lines)

            for line in sql_lines:
                if re.search('KEY', line) or re.search('PRIMARY', line) \
                        or re.search('"ID"', line) or line.startswith('CREATE') \
                        or line.startswith(')'):
                    continue

                hit = re.search(r'(\S+)\ ([\w\d]+(\(.*?\))?) ?.*?$', line)
                if hit is not None:

                    name, d_type = hit.group(1), hit.group(2)
                    d_type = re.sub(r'(\w+)\(.*', r'\1', d_type)
                    name = str(re.sub('`', '', name))
                    if name in fks.keys():
                        if fks[name][1].lower() == 'id':
                            field_type = 'reference %s' % (fks[name][0])
                        else:
                            field_type = 'reference %s.%s' % (
                                fks[name][0], fks[name][1])
                    else:
                        field_type = data_type_map.get(d_type.lower())
                        if field_type is None:
                            continue

                    web2py_table_code += "\n    Field('%s','%s')," % (
                        name, field_type)
            web2py_table_code = "db.define_table('%s',%s\n    migrate=False)" % (
                table_name, web2py_table_code)
            legacy_db_table_web2py_code.append(web2py_table_code)

    # ----------------------------------------
    # write the legacy db to file
    legacy_db_web2py_code = connection_string + "\n\n"
    legacy_db_web2py_code += "\n\n#--------\n".join(
        legacy_db_table_web2py_code)
    return legacy_db_web2py_code


def extract_models(db_path: str, output_file: str):
    db_string = sqlite(db_path)
    with open(f'{output_file}.py', 'w') as file:
        file.write(header)
        file.writelines(db_string)
        file.write('')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE:\n\n    extract_mysql_models.py data_basename output_file.py \n\n')
    else:
        # db_string = sqlite(sys.argv[1])
        output_file = sys.argv[-1]
        extract_models(sys.argv[1], output_file)
        print(f'file {output_file}.py created')
