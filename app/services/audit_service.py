import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(slots=True)
class AuditEvent:
    request_id: str
    user_id: int
    input_size: int
    status: str
    result_url: str | None = None
    error_code: str | None = None


class AuditService:
    def __init__(self) -> None:
        self._logger = logging.getLogger("audit")

    @staticmethod
    def new_request_id() -> str:
        return str(uuid4())

    def log(self, event: AuditEvent) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": event.request_id,
            "user_id": event.user_id,
            "input_size": event.input_size,
            "status": event.status,
            "result_url": event.result_url,
            "error_code": event.error_code,
        }
        self._logger.info("audit_event=%s", payload)

