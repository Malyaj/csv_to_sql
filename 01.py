# -*- coding: utf-8 -*-
"""
Script to functionalize conversion of standard table csv to sql queries
"""

import os
import pandas as pd


def query_create(filepath, table_name=None, primary=None, null=None):
    '''
    filepath to the csv file
    returns the sql query to create table
    tailored for postgresql
    may work elsewhere as well
    '''
    
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(filepath))[0]
    
    df = pd.read_csv(filepath)



    create_query = """
    CREATE TABLE {table_name} (
    """.format_map({'table_name':table_name})
    
    field_headers = list(df.columns) ## extracted from the csv file
    field_types = ['INT', 'VARCHAR(150)', 'VARCHAR(150)', 'VARCHAR(150)', 'VARCHAR(7)', 'INT'] ## can these be infered ?
    primary_flag = [True, False, False, False, False, False]  # could be passed as a list of column names to be inferred as primary key
    non_null_flag = [True, True, True, False, True, True]  # could be based on fields having or not having missing values ?
    
    def primary(bool_val):
        if bool_val:
            return 'PRIMARY KEY'
        return ''
    
    def non_null(bool_val):
        if bool_val:
            return 'NOT NULL'
        return ''
    
    
    primary_flag = list(map(primary,primary_flag))
    non_null_flag = list(map(non_null, non_null_flag))
    
    suffix = ',\n'
    
    for each in zip(field_headers, field_types, primary_flag, non_null_flag):
        create_query = create_query + ' '.join(list(each)) + suffix
    
    create_query = create_query.strip()[:-1]
    create_query = create_query + '\n);'
        
    return create_query

## collect parameters
path = os.path.dirname(__file__)
os.chdir(path)
filename = 'janta.csv'
filepath = os.path.join(path, filename)

## call the function
query = query_create(filepath)

## write the query to a sql file
sqlfilepath = os.path.join(path, 'query.sql')

with open(sqlfilepath, 'w') as f:
    f.write(query)

