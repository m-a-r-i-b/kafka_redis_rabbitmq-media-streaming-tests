from confluent_kafka.admin import AdminClient, NewTopic, ConfigResource

n_repicas = 1
n_partitions = 1

admin_client = AdminClient({
    "bootstrap.servers": "localhost:9092"
})

topic_list = []
topic_list.append(NewTopic("multi-video-stream", n_partitions, n_repicas,config={'max.message.bytes':'20000000'}))
# topic_list.append(NewTopic("multi-video-stream", n_partitions, n_repicas,config={'retention.bytes': '50000000', 'segment.bytes': '20000000' }))
# topic_list.append(NewTopic("multi-video-stream", n_partitions, n_repicas,config={'cleanup.policy': 'delete', 'retention.ms': '30000', 'delete.retention.ms': '30000', 'segment.bytes': '20000000'  }))
# topic_list.append(NewTopic("multi-video-stream", n_partitions, n_repicas,config={'cleanup.policy': 'delete', 'retention.ms': '30000', 'segment.bytes': '20000000'  }))
fs = admin_client.create_topics(topic_list)

print()

for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))