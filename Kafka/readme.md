
# Kafka Data Pipeline with MySQL Integration

This project demonstrates how to use Kafka producers and consumers to handle data and insert it into a MySQL database, partitioned by year. It consists of four main scripts:

- **kafka-config.py**: Configuration file for Kafka producer and consumer.
- **kafka-producer.py**: Sends data to a Kafka topic.
- **kafka-consumer.py**: Consumes data from the Kafka topic and inserts it into MySQL.
- **kafka-db.py**: Creates the necessary database table in MySQL where the consumer will insert the data.

## Requirements

- Kafka cluster running (localhost:9092 by default).
- MySQL server running with access to a database.
- Python 3.x with the following dependencies:
  - `kafka-python`
  - `mysql-connector-python`
  - `python-dotenv`
  - `pandas`

## Setup Instructions

### 1. **Configure MySQL Database**

Before running the consumer, ensure your MySQL database is set up:

1. Create a `.env` file in the project root and provide your MySQL credentials:

   ```
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=your_db_host
   DB_NAME=your_db_name
   ```

2. Run the `kafka-db.py` script to create the `Fundamental_data` table, partitioned by year. This will automatically set up the table with the appropriate partitions for data insertion.

   ```bash
   python kafka-db.py
   ```

   This will create the table `Fundamental_data` in the `KafkaDB` database.

### 2. **Running the Kafka Producer**

The producer script (`kafka-producer.py`) sends data to the Kafka topic. You can run this script to simulate sending data to the Kafka topic:

```bash
python kafka-producer.py
```

### 3. **Running the Kafka Consumer**

The consumer script (`kafka-consumer.py`) listens to the Kafka topic and inserts data into MySQL. Run this script to consume data and insert it into the database:

```bash
python kafka-consumer.py
```

The consumer will process messages in chunks and insert them into the `Fundamental_data` table.

## Additional Notes

- **Partitions**: The MySQL table `Fundamental_data` is partitioned by year, which helps optimize data insertion and querying based on the year.
- **Kafka Configuration**: The Kafka producer and consumer are set up to communicate with a Kafka cluster running locally (`localhost:9092`). Adjust this if your Kafka cluster is located elsewhere.


