from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer
import logging

# Kafka broker address
BROKER = 'localhost:9092'
client_id='admin'

# logging.basicConfig(filename='kafka-config.log', encoding='utf-8',
#                     level=logging.INFO)

def list_topics():
    k_client = KafkaAdminClient(bootstrap_servers=BROKER,client_id=client_id)
    topics = k_client.list_topics()
    print(f"topics: {topics}")
    k_client.close()

def describe_topic(topic_name):
    consumer = KafkaConsumer(bootstrap_servers=BROKER)
    topic_metadata = consumer.topics()
    if topic_name in topic_metadata:
        partitions = consumer.partitions_for_topic(topic_name)
        print(f"topic: {topic_name} partitions: {partitions}")
    else:
        pass
    consumer.close()

def create_topic(topic_name, num_partitions=1, replication_factor=1):
    k_client = KafkaAdminClient(bootstrap_servers=BROKER, client_id=client_id)
    try:
        topic = NewTopic(name=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
        k_client.create_topics(new_topics=[topic], validate_only=False)
        print(f"topic: {topic_name} created successfully.")
    except Exception as e:
        print("error creating topic")
        pass
    finally:
        k_client.close()

def delete_topic(topic_name):
    k_client = KafkaAdminClient(bootstrap_servers=BROKER, client_id=client_id)
    try:
        k_client.delete_topics([topic_name])
        print(f"topic: {topic_name} deleted successfully.")
    except Exception as e:
        print("error deleting topic")
        pass
    finally:
        k_client.close()


topic_name = 'fundamental_data'

create_topic(topic_name, num_partitions=10, replication_factor=1)
describe_topic(topic_name)

# delete_topic(topic_name)
list_topics()