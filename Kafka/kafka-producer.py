from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging as log

import numpy as np
import pandas as pd
from tqdm import tqdm
import json

ticker_data = pd.read_csv("ind_nifty50list.csv")[['Industry', 'Symbol']]
fundamental_data = pd.read_csv("Fundamental_Data.csv")
ticker_data.rename(columns={'Industry':'industry', 'Symbol':'stock_symbol'},inplace=True)
fundamental_data = pd.merge(fundamental_data,ticker_data,on='stock_symbol',
                        how="inner")
fundamental_data = fundamental_data[fundamental_data['year']>=2014]



chunk_sz = 100
record_sz = fundamental_data.shape[0]
print(f"record_sz : {record_sz}")
# records = list(fundamental_data.itertuples(index=False, name=None)) 

# Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

for idx in tqdm(range(0,record_sz,chunk_sz)):
  if idx+chunk_sz>=record_sz:
      data = fundamental_data[idx:]
      data_json = data.to_json(orient='records')
      print(f"{idx} records sent with chunk_sz {len(data)}")
      # logger.debug(f"last_chunk : {data.shape[0]}")
  else:
      data = fundamental_data[idx:idx+chunk_sz]   
      data_json = data.to_json(orient='records')
  key = str(idx % 10).encode('utf-8')  # round-robin - update kafka-config
  producer.send('fundamental_data', key=key, value=data_json.encode('utf-8'))
  if idx % 1000 == 0:
    print(f"sent {idx} records successfully.")

# flush producer ensures all messages are sent
producer.flush()
print("all records sent successfully.")

