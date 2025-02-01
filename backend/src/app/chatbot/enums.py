import enum


class ChatMessageResponseStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    DELETED = "deleted"
