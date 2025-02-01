import enum


class ChatResponseStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"
