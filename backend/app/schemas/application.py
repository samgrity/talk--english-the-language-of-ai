from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.core.enums import (
    CompanyVerificationStatus,
    CompanyType,
    Department,
    SubDepartment,
    UpdateActor,
    UpdateType,
)


class Address(BaseModel):
    address1: str
    country: str
    id: str
    locality: str
    postalCode: str
    region: str


class Company(BaseModel):
    id: str
    name: str
    siteUrl: str
    size: str
    type: CompanyType
    verificationStatus: CompanyVerificationStatus
    address: Address


class LocaleInfo(BaseModel):
    country: str
    preferredLanguage: str
    region: str
    storeId: str


class Update(BaseModel):
    id: str
    timestamp: datetime
    actor: UpdateActor
    internal_notes: str
    recruiter_id: str | None = None
    update_type: UpdateType
    correspondence: str | None = None

    model_config = ConfigDict(from_attributes=True)


class Application(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    mobile: str
    bio: str
    linkedinUrl: str
    currentRole: str
    seniorityLevel: str
    jobTitle: str
    department: Department
    subDepartments: list[SubDepartment]
    companyId: str
    company: Company
    assignee_id: str | None = None
    region: str | None = None
    screeningStatus: str
    createdAt: datetime
    updatedAt: datetime
    locale: LocaleInfo
    updates: list[Update] = []


class ApplicationSummary(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    mobile: str
    jobTitle: str
    seniorityLevel: str
    department: Department
    companyName: str
    companySize: str
    companyType: str
    region: str
    assignee_id: str | None = None
    assignee_name: str | None = None
    screeningStatus: str
    createdAt: datetime
    updatedAt: datetime


class StatusUpdateRequest(BaseModel):
    status: str


class NewUpdateRequest(BaseModel):
    update_type: UpdateType
    internal_notes: str
    recruiter_id: str
    correspondence: str | None = None


class ApplicationUpdateRequest(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    mobile: str | None = None
    bio: str | None = None
    linkedinUrl: str | None = None
    jobTitle: str | None = None
    seniorityLevel: str | None = None
    department: Department | None = None
    subDepartments: list[SubDepartment] | None = None
    region: str | None = None
    assignee_id: str | None = None
    companyName: str | None = None
    companySize: str | None = None
    companyType: CompanyType | None = None
    companyVerificationStatus: CompanyVerificationStatus | None = None
    companySiteUrl: str | None = None
