// TypeScript interfaces matching the backend API responses

export enum Department {
  ENGINEERING = "ENGINEERING",
  PRODUCT = "PRODUCT",
  DESIGN = "DESIGN",
  MARKETING = "MARKETING",
  SALES = "SALES",
  FINANCE = "FINANCE",
  OPERATIONS = "OPERATIONS",
  LEGAL = "LEGAL"
}

export enum SubDepartment {
  ENG_BACKEND = "ENG_BACKEND",
  ENG_FRONTEND = "ENG_FRONTEND",
  ENG_INFRA = "ENG_INFRA",
  ENG_DATA = "ENG_DATA",
  ENG_SECURITY = "ENG_SECURITY",
  PROD_MOBILE = "PROD_MOBILE",
  PROD_WEB = "PROD_WEB",
  PROD_GROWTH = "PROD_GROWTH",
  DES_UX = "DES_UX",
  DES_UI = "DES_UI",
  DES_RESEARCH = "DES_RESEARCH",
  MKT_CONTENT = "MKT_CONTENT",
  MKT_GROWTH = "MKT_GROWTH",
  MKT_BRAND = "MKT_BRAND"
}

export enum FilterStatus {
  PENDING = "pending",
  COMPLETED = "completed",
  WITHDRAWN = "withdrawn",
  ALL = "all",
  WAITING_FOR_RECRUITER = "waiting_for_recruiter",
  WAITING_FOR_AI = "waiting_for_ai",
  WAITING_FOR_CANDIDATE = "waiting_for_candidate",
  ADVANCED = "advanced",
  DECLINED = "declined"
}

export interface Address {
  address1: string;
  country: string;
  id: string;
  locality: string;
  postalCode: string;
  region: string;
}

export interface HiringCompany {
  id: string;
  name: string;
  siteUrl: string;
  size: string;
  address: Address;
}

export interface JobOpening {
  title: string;
  seniorityLevel: 'Senior' | 'Mid' | 'Junior';
  department: Department;
  subDepartments: SubDepartment[];
  jobDescription: string;
  company: HiringCompany;
}

export interface LocaleInfo {
  country: string;
  preferredLanguage: string;
  region: string;
  storeId: string;
}

export interface Recruiter {
  id: string;
  name: string;
}

export interface Update {
  id: string;
  timestamp: string;
  actor: 'ai_agent' | 'human_recruiter' | 'candidate';
  internal_notes: string;
  recruiter_id?: string;
  update_type: 'recommend_advance' | 'recommend_decline' | 'recommend_follow_up' | 'advance' | 'decline' | 'follow_up' | 'request_ai_screen' | 'general_update';
  correspondence?: string;
}

export interface Application {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  mobile: string;
  bio: string;
  linkedinUrl: string;
  jobOpening: JobOpening;
  assignee_id?: string;
  region?: string;
  screeningStatus: 'waiting_for_recruiter' | 'waiting_for_ai' | 'waiting_for_candidate' | 'advanced' | 'declined' | 'withdrawn';
  createdAt: string;
  updatedAt: string;
  locale: LocaleInfo;
  updates: Update[];
}

export interface ApplicationSummary {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  mobile: string;
  jobTitle: string;
  seniorityLevel: string;
  department: Department;
  companyName: string;
  region: string;
  assignee_id?: string;
  assignee_name?: string;
  screeningStatus: string;
  createdAt: string;
  updatedAt: string;
}

export interface StatusUpdateRequest {
  status: string;
}

export interface NewUpdateRequest {
  update_type: string;
  internal_notes: string;
  recruiter_id?: string;
  correspondence?: string;
}

export interface ApplicationUpdateRequest {
  firstName?: string;
  lastName?: string;
  email?: string;
  mobile?: string;
  bio?: string;
  linkedinUrl?: string;
  jobTitle?: string;
  seniorityLevel?: string;
  department?: Department;
  subDepartments?: SubDepartment[];
  jobDescription?: string;
  region?: string;
  assignee_id?: string;
  companyName?: string;
  companySize?: string;
  companySiteUrl?: string;
}
