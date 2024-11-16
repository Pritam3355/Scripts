import os
import json
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
from mysql.connector import connect
from dotenv import load_dotenv



load_dotenv()

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME')
}


def insert_data(data):
    conn = connect(**db_config)
    cursor = conn.cursor()
    # list of dictionaries to list of tuples
    rows = [(
        d['category'], d['report_type'], d['stock_symbol'],
        d['year'], d['month'], d['value_type'], d['industry']
    ) for d in data]
    
    # Execute batch insert
    cursor.executemany('''
        INSERT INTO KafkaDB.Fundamental_data 
        (category, report_type, stock_symbol, year, month, value_type, industry)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', rows)
    conn.commit()
    cursor.close()
    conn.close()


chunk_sz = 1000
records = [] # buffer
fundamental_data = pd.read_csv("Fundamental_Data.csv")
fundamental_data = fundamental_data[fundamental_data['year']>=2014]
record_sz = fundamental_data.shape[0]
print(f"record_sz : {record_sz}")
print(f"total complete chunks : {record_sz//chunk_sz}")
chunk_cnt = 0

# Kafka Consumer setup
consumer = KafkaConsumer(
    'fundamental_data',
    group_id='fundamental_group',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    enable_auto_commit=True,
    auto_offset_reset='earliest'
)


try:
    for idx, message in enumerate(consumer):
        # message.value is a list of dictionaries - add it to buffer
        records.extend(message.value)  # 
        if len(records) >= chunk_sz and chunk_cnt!=record_sz//chunk_sz:
            insert_data(records[:chunk_sz])
            records = records[chunk_sz:]  # update buffer
            chunk_cnt +=1
            print(f"inserted upto {chunk_cnt*chunk_sz} records successfully")

        elif chunk_cnt>=record_sz//chunk_sz and len(records)>0:
        	left_over_chunk = len(records) 
        	insert_data(records[:left_over_chunk])
        	records = records[left_over_chunk:]
        	print(f"inserted remaining {left_over_chunk} records successfully")
        	
except KeyboardInterrupt:
    print("consumer interrupted...")
finally: # insert remaining records on interrupt
	# if records:
	# 	insert_data(records)
	# 	print(chunk_cnt)
	consumer.close()
	print(f"consumer closed.")
