import json
import pika
from fastapi import FastAPI

from app.models import TaskResponse, SubjectRequest, ResultResponse

app = FastAPI()

def get_channel():
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
    return connection, channel




@app.post("/v1", response_model=TaskResponse)
def create_task(subject: SubjectRequest):
    task_uuid = subject.uuid
    result_queue = f'result_{task_uuid}'

    connection, channel = get_channel()
    try:
        channel.queue_declare(
            queue=result_queue,
            durable=False,
            auto_delete=True
        )

        task_data = {
            'uuid': task_uuid,
            'subject_name': subject.subject_name,
            'subject_description': subject.subject_description,
            'blocks': subject.blocks,  # уже list[dict]
            'archives': subject.archives,
            'result_queue': result_queue
        }

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(task_data, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

        return TaskResponse(
            uuid=task_uuid,
            status='processing',
            result_queue=result_queue
        )

    finally:
        connection.close()


@app.get("/v1/task/{task_uuid}", response_model=ResultResponse)
def get_result(task_uuid: str):
    result_queue = f'result_{task_uuid}'

    connection, channel = get_channel()

    try:
        try:
            channel.queue_declare(
                queue=result_queue,
                passive=True
            )
        except Exception:
            return ResultResponse(uuid=task_uuid, status='processing')

        method_frame, properties, body = channel.basic_get(
            queue=result_queue,
            auto_ack=True
        )

        if method_frame:
            result = json.loads(body.decode('utf-8'))
            return ResultResponse(**result)
        else:
            return ResultResponse(uuid=task_uuid, status='processing')

    finally:
        connection.close()