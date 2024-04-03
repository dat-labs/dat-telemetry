import dat_client
from dat_client.rest import ApiException
from dat_client.models.message import Message
from dat_client.models.stack_trace import StackTrace
from dat_client.configuration import Configuration
from dat_client.models.dat_log_message import DatLogMessage
from dat_client.models.dat_log_message_level import DatLogMessageLevel

from .pydantic_models.telemetry_msg import TelemetryMsg


class BaseTelemetryHandler:
    def __init__(self) -> None:
        pass

    def process_msg(self) -> None:
        raise NotImplementedError


class DBTelemetryHandler(BaseTelemetryHandler):
    def __init__(self) -> None:
        super().__init__()
        self.configuration = Configuration(
            host="http://api:8000",
            # verify_ssl=False,
        )

    def process_msg(self, telemetry_msg: TelemetryMsg) -> None:
        with dat_client.ApiClient(self.configuration) as api_client:
            conn_run_log_api_instance = dat_client.ConnectionRunLogsApi(
                api_client)
            try:
                api_response = conn_run_log_api_instance.add_connection_run_log_connection_run_logs_post(
                    connection_id=telemetry_msg.connection_id,
                    dat_log_message=DatLogMessage.from_json(
                        telemetry_msg.dat_message.log.model_dump_json()
                    ),
                )
                print(
                    "The response of ConnectionRunLogsApi->add_connection_run_log_connection_run_logs_post:\n")
                print(api_response)
            except ApiException as e:
                print(
                    "Exception when calling ConnectionRunLogsApi->add_connection_run_log_connection_run_logs_post: %s\n" % e)
