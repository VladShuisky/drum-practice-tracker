import asyncio
import aio_pika
import django
import os
from asgiref.sync import sync_to_async
import dotenv
dotenv.load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drum_practice_tracker.settings")
django.setup()

RABBITMQ_DEFAULT_USER=os.environ.get('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS=os.environ.get('RABBITMQ_DEFAULT_PASS')
RABBIT_MQ_PORT=os.environ.get('RABBIT_MQ_PORT')
RABBIT_MQ_CONTAINER=os.environ.get('RABBIT_MQ_CONTAINER')


from users.models import User, Stats
from training.models import TrainingSession
from django.utils import timezone

@sync_to_async
def update_stats(user_id: int):
    user = User.objects.get(pk=user_id)
    sessions = TrainingSession.objects.filter(user=user)

    total_sessions = sessions.count()
    total_minutes = sum(s.duration_minutes for s in sessions)
    avg_duration = total_minutes / total_sessions if total_sessions else 0

    stats, _ = Stats.objects.get_or_create(user=user)
    stats.total_sessions = total_sessions
    stats.total_minutes = total_minutes
    stats.avg_duration = avg_duration
    stats.last_calculated_at = timezone.now()
    stats.save()

    return user.username


async def handle_message(message: aio_pika.IncomingMessage):
    async with message.process(): # <<< ЗДЕСЬ происходить ack автоматически!
        body = message.body.decode()
        event, user_id = body.split(":")
        user_id = int(user_id)

        if event == "training.session_created":
            username = await update_stats(user_id)
            print(f"[x] Stats updated for {username}")


async def connect():
    while True:
        try:
            return await aio_pika.connect_robust(
                f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBIT_MQ_CONTAINER}:{RABBIT_MQ_PORT}/"
                )
        except Exception as e:
            print(f"RabbitMQ not ready, retrying in 5s... ({e})")
            await asyncio.sleep(5)

async def main():
    connection = await connect()
    channel = await connection.channel()
    queue = await channel.declare_queue("training_events", durable=True)
    await queue.consume(handle_message)
    print("[*] Waiting for messages. To exit press CTRL+C")
    return connection


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    connection = loop.run_until_complete(main())
    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
