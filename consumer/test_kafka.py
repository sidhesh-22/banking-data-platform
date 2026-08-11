from kafka import KafkaAdminClient

admin = KafkaAdminClient(
    bootstrap_servers="localhost:29092",
    client_id="test"
)

print(admin.list_topics())

admin.close()