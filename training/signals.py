import pika
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TrainingSession


def publish_event(user_id):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="drums_rabbitmq", credentials=pika.PlainCredentials('admin', 'admin')) # TODO вынести в env, или подтянуть из env
    )
    channel = connection.channel()
    channel.queue_declare(queue="training_events", durable=True)

    message_body = f"training.session_created:{user_id}"
    channel.basic_publish(
        exchange="",
        routing_key="training_events",
        body=message_body.encode(),
        properties=pika.BasicProperties(delivery_mode=2)  # persist
    )
    connection.close()

@receiver(post_save, sender=TrainingSession)
def trigger_event(sender, instance, created, **kwargs):
    if created:
        publish_event(instance.user.id)