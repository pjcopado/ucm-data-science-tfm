import enum


class ChatMessageResponseStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    QUERY_INVALID = "query_invalid"
    QUERY_COMPLETED = "query_completed"
    QUERY_FAILED = "query_failed"
    QUERY_EXECUTION_COMPLETED = "query_execution_completed"
    QUERY_EXECUTION_FAILED = "query_execution_failed"
    INSIGHT_COMPLETED = "insight_completed"
    INSIGHT_FAILED = "insight_failed"
    COMPLETED = "completed"
    ERROR = "error"

    def list():
        return [item.value for item in ChatMessageResponseStatusEnum]
