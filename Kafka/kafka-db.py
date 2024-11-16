import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME')
}

def create_tables():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS KafkaDB.Fundamental_data(
            id INT NOT NULL AUTO_INCREMENT,
            category VARCHAR(255), 
            report_type VARCHAR(50),
            stock_symbol VARCHAR(50),
            year INT NOT NULL,
            month INT,
            value_type FLOAT,
            industry VARCHAR(255),
            PRIMARY KEY (id, year)
            ) 
        PARTITION BY RANGE (year)(
            PARTITION p2014 VALUES LESS THAN (2015),
            PARTITION p2015 VALUES LESS THAN (2016),
            PARTITION p2016 VALUES LESS THAN (2017),
            PARTITION p2017 VALUES LESS THAN (2018),
            PARTITION p2018 VALUES LESS THAN (2019),
            PARTITION p2019 VALUES LESS THAN (2020),
            PARTITION p2020 VALUES LESS THAN (2021),
            PARTITION p2021 VALUES LESS THAN (2022),
            PARTITION p2022 VALUES LESS THAN (2023),
            PARTITION p2023 VALUES LESS THAN (2024),
            PARTITION p2024 VALUES LESS THAN (2025)
            -- PARTITION future VALUES LESS THAN MAXVALUE
            )
    ''')
    print("Table Fundamental_data(partitioned on years)  created")
    conn.commit()
    cursor.close()
    conn.close()
    
create_tables()
