"""
Entry point module for dat pipeline worker
"""
from celery import Celery
from .pydantic_models.telemetry_msg import TelemetryMsg
import pydantic_core
from .std_lib import DBTelemetryHandler


jobs_celery_app = Celery(broker='amqp://mq_user:mq_pass@message-queue:5672//')


@jobs_celery_app.task(queue='dat-telemetry-q', name='dat_telemetry_task')
def worker(dat_telemetry_msg_str):
    '''celery worker
    Args:
        dat_telemetry_msg_str (str)
    '''
    try:
        dat_telemetry_msg = TelemetryMsg.model_validate_json(
            dat_telemetry_msg_str)
    except pydantic_core._pydantic_core.ValidationError as _e:
        print(f'{_e}: {dat_telemetry_msg_str}')
        raise

    print(f'Received msg with dat_telemetry_msg_str: {dat_telemetry_msg_str}')

    # Call API via SDK to log connection runs to backend db
    DBTelemetryHandler().process_msg(dat_telemetry_msg)


if __name__ == '__main__':
    jobs_celery_app.send_task('dat_telemetry_task', (open(
        'msg.json').read(), ), queue='dat-telemetry-q')
