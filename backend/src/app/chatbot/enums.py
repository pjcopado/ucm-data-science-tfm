import enum


class ChatMessageResponseStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    DELETED = "deleted"


class InsightModelEnum(str, enum.Enum):
    HUGGINGFACE = "google/flan-t5-xl"
