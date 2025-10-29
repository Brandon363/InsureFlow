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
    PAYMENT_UPDATE = 'PAYMENT_UPDATE'
    CLAIM_UPDATE = 'CLAIM_UPDATE'
    POLICY_UPDATE = 'POLICY_UPDATE'
    ANNOUNCEMENT = 'ANNOUNCEMENT'
    USER_UPDATE = 'USER_UPDATE'
    APPLICATION_UPDATE = 'APPLICATION_UPDATE'


class NotificationStatus(str, Enum):
    UNREAD = 'UNREAD'
    READ = 'READ'
    ARCHIVED = 'ARCHIVED'


class DocumentType(str, Enum):
    CLAIM_DOCUMENT = "CLAIM_DOCUMENT"  # Claim-related documents
    SUPPORTING_DOCUMENT = "SUPPORTING_DOCUMENT"  # Personal documents like IDs, licenses, etc.
    NATIONAL_ID = "NATIONAL_ID"

class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    RESUBMITTED = "RESUBMITTED"

class ClaimType(str, Enum):
    TEMPORARY_LOSS_OF_INCOME = "Temporary Loss of Income"
    PERMANENT_DISABILITY = "Permanent Disability"
    CRITICAL_ILLNESS = "Critical Illness"
    HOSPITALIZATION = "Hospitalization"
    SURGICAL = "Surgical"
    DEATH_BENEFIT = "Death Benefit"
    ACCIDENTAL_DEATH = "Accidental Death"
    OTHER = "Other"

class ApplicationStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    DECLINED = "Declined"
    IN_PROGRESS = "In Progress"


class TrackingStatus(str, Enum):
    CURRENT = "Current"
    COMPLETED = "Completed"
    PENDING = "Pending"


class ApplicationStage(str, Enum):
    SUBMITTED = "Submitted"
    DOCUMENTS_VERIFIED = "Documents Verified"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    DECLINED = "Declined"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class VerificationTrackingStage(str, Enum):
    SUBMITTED = "Submitted"
    RESUBMITTED = "Resubmitted"
    DOCUMENTS_VERIFIED = "Documents Verified"
    UNDER_REVIEW = "Under Review"
    APPROVED = "Approved"
    DECLINED = "Declined"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"