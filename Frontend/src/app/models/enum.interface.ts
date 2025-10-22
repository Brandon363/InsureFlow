export enum EntityStatus {
  ACTIVE = "ACTIVE",
  INACTIVE = "INACTIVE",
  DELETED = "DELETED"
}

export enum PolicyType {
  AUTO = "AUTO",
  HOME = "HOME",
  LIFE = "LIFE",
  HEALTH = "HEALTH"
}

export enum PolicyStatus {
  ACTIVE = "ACTIVE",
  PENDING = "PENDING",
  EXPIRED = "EXPIRED",
  CANCELLED = "CANCELLED"
}

export enum ClaimStatus {
  SUBMITTED = "SUBMITTED",
  IN_REVIEW = "IN_REVIEW",
  APPROVED = "APPROVED",
  REJECTED = "REJECTED",
  PAID = "PAID"
}

export enum PaymentStatus {
  PENDING = "PENDING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
  REFUNDED = "REFUNDED"
}

export enum PaymentMethod {
  CREDIT_CARD = "CREDIT_CARD",
  BANK_TRANSFER = "BANK_TRANSFER",
  MOBILE_MONEY = "MOBILE_MONEY"
}

export enum UserRole {
  ADMIN = "ADMIN",
  AGENT = "AGENT",
  CUSTOMER = "CUSTOMER"
}

export enum NotificationType {
  PAYMENT_DUE = "PAYMENT_DUE",
  CLAIM_UPDATE = "CLAIM_UPDATE",
  POLICY_UPDATE = "POLICY_UPDATE",
  ANNOUNCEMENT = "ANNOUNCEMENT"
}

export enum NotificationStatus {
  UNREAD = "UNREAD",
  READ = "READ",
  ARCHIVED = "ARCHIVED"
}

export enum DocumentType {
  CLAIM_DOCUMENT = "CLAIM_DOCUMENT",
  SUPPORTING_DOCUMENT = "SUPPORTING_DOCUMENT",
  NATIONAL_ID = "NATIONAL_ID"
}