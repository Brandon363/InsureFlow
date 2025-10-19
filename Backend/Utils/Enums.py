from enum import Enum

class EntityStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class PolicyType(str, Enum):
    AUTO = 'AUTO',
    HOME = 'HOME',
    LIFE = 'LIFE',
    HEALTH = 'HEALTH'


class PolicyStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    PENDING = 'PENDING'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'


class ClaimStatus(str, Enum):
    SUBMITTED = 'SUBMITTED'
    IN_REVIEW = 'IN_REVIEW'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    PAID = 'PAID'


class PaymentStatus(str, Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    REFUNDED = 'REFUNDED'


class PaymentMethod(str, Enum):
    CREDIT_CARD = 'CREDIT_CARD'
    BANK_TRANSFER = 'BANK_TRANSFER'
    MOBILE_MONEY = 'MOBILE_MONEY'


class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    AGENT = 'AGENT'
    CUSTOMER = 'CUSTOMER'


class NotificationType(str, Enum):
    PAYMENT_DUE = 'PAYMENT_DUE'
    CLAIM_UPDATE = 'CLAIM_UPDATE'
    POLICY_UPDATE = 'POLICY_UPDATE'
    ANNOUNCEMENT = 'ANNOUNCEMENT'


class NotificationStatus(str, Enum):
    UNREAD = 'UNREAD'
    READ = 'READ'
    ARCHIVED = 'ARCHIVED'


class DocumentType(str, Enum):
    CLAIM_DOCUMENT = "CLAIM_DOCUMENT"  # Claim-related documents
    SUPPORTING_DOCUMENT = "SUPPORTING_DOCUMENT"  # Personal documents like IDs, licenses, etc.