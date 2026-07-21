import json
import os
import pika
from worker.ai import AI
from worker.prompts import prompt_for_annotation
from worker.utiles import decode_base64_data, extract_zip_data

username = os.getenv('RABBIT_USERNAME')
password = os.getenv('RABBIT_PASSWORD')
host = os.getenv('RABBIT_HOST')
port = os.getenv('RABBIT_PORT')
task_queue = os.getenv('RABBIT_TASK_QUEUE')
result_queue = os.getenv('RABBIT_RESULT_QUEUE')

credentials = pika.PlainCredentials('myuser', 'mypassword')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=credentials
    )
)
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
channel.basic_qos(prefetch_count=1)


def work(body):
    result = {}
    bytes_archives = decode_base64_data(body['archives'])
    data = extract_zip_data(bytes_archives)
    ai = AI()
    result['blocks'] = ai.orchestrate_course_generation(body['blocks'], data)
    result['annotation'] = ai.request_to_qwen(data, prompt_for_annotation)['annotation']
    return result


def callback(ch, method, properties, body):
    task_data = json.loads(body.decode('utf-8'))
    task_uuid = task_data['uuid']

    print(f" [x] Получена задача: {task_uuid}")

    try:
        result = work(task_data)
        response = {
            'uuid': task_uuid,
            'status': 'completed',
            'result': result
        }

    except Exception as e:
        response = {
            'uuid': task_uuid,
            'status': 'error',
            'error': str(e)
        }
    ch.basic_publish(
        exchange='',
        routing_key=result_queue,
        body=json.dumps(response, ensure_ascii=False),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        )
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()