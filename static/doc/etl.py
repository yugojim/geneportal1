# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 11:20:49 2024

@author: 11107045
"""
import psycopg2
import json 
#PostgreSQL
import pandas as pd

def flatten_dict(d):
    flattened_dict = {}

    def flatten(item, key=''):
        if isinstance(item, dict):
            for sub_key, sub_item in item.items():
                flatten(sub_item, key + sub_key + '_')
        elif isinstance(item, list):
            for i, sub_item in enumerate(item):
                flatten(sub_item, key + str(i) + '_')
        else:
            flattened_dict[key[:-1]] = item

    flatten(d)
    return flattened_dict

def unflatten_dict(flat_dict):
    unflattened_dict = {}
    for key, value in flat_dict.items():
        parts = key.split('_')  # 拆分键名中的点号
        current_dict = unflattened_dict
        for part in parts[:-1]:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        current_dict[parts[-1]] = value
    return unflattened_dict

# 读取 Excel 文件
df = pd.read_excel('FHIR第三版.xlsx')

# 打印 DataFrame 的内容
table=[]
column=[]
#print(df[' 資料庫.欄位名稱'])
for di in range(len(df[' 資料庫.欄位名稱'])):
    table.append(df[' 資料庫.欄位名稱'][di].split('.')[0])
    column.append(df[' 資料庫.欄位名稱'][di].split('.')[1])
print(table,column)

ip='10.221.252.50'
port='5432'
database='BASE'
username='wiadvance'
password='TEpVSENLaFBkCg'

jsonPath='Resource.json'
cancerflattenjson = json.load(open(jsonPath,encoding="utf-8"))
list_of_key = list(cancerflattenjson.keys())
list_of_value = list(cancerflattenjson.values())
jsonPath='Roche_example0412.json'
cancerbasejson = json.load(open(jsonPath,encoding="utf-8"))
flattencancerbasejson=flatten_dict(cancerbasejson)
#conn = psycopg2.connect(database='', user='ID', password='PassWord', host='IP', port='Port')
#cur = conn.cursor()
#consentsql = "SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'reportxml';"
#cur.execute(consentsql)
#rows = cur.fetchall()

#print(len(rows))
for i in range(len(list_of_value)):
    if 'SQL' in str(list_of_value[i]):
        keylist=str(list_of_key[i]).split('_')
        #print(str(list_of_value[i]).split('_'))
        
        #sqlstr='select ' + list_of_value[i].split('_')[2] + ' from ' + list_of_value[i].split('_')[1]
        #cur.execute(sqlstr)
        #rows = cur.fetchall()
        for key in keylist:
            cancerbasejson['identifier']['use']
