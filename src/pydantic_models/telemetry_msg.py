from pydantic import BaseModel
from dat_core.pydantic_models.dat_message import DatMessage


class TelemetryMsg(BaseModel):
    connection_id: str
    run_id: str
    dat_message: DatMessage
