import { Application, ApplicationSummary, StatusUpdateRequest, NewUpdateRequest, ApplicationUpdateRequest, Recruiter } from '@/types/api';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:8000";

export async function getApplications(filter?: string, search?: string): Promise<ApplicationSummary[]> {
  const params = new URLSearchParams();
  if (filter) params.append('filter', filter);
  if (search && search.trim()) params.append('search', search.trim());

  const url = `${BACKEND_URL}/api/applications${params.toString() ? '?' + params.toString() : ''}`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to fetch applications: ${response.status}`);
  }
  return response.json();
}

export async function getApplication(id: string): Promise<Application> {
  const response = await fetch(`${BACKEND_URL}/api/applications/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to fetch application: ${response.status}`);
  }
  return response.json();
}

export async function updateApplicationStatus(id: string, request: StatusUpdateRequest): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/applications/${id}/status`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Failed to update application status: ${response.status}`);
  }
}

export async function addUpdate(id: string, request: NewUpdateRequest): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/applications/${id}/updates`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Failed to add update: ${response.status}`);
  }
}

export async function updateApplication(id: string, request: ApplicationUpdateRequest): Promise<void> {
  const response = await fetch(`${BACKEND_URL}/api/applications/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  });
  if (!response.ok) {
    throw new Error(`Failed to update application: ${response.status}`);
  }
}

export async function getRecruiters(): Promise<Recruiter[]> {
  const response = await fetch(`${BACKEND_URL}/api/recruiters`);
  if (!response.ok) {
    throw new Error(`Failed to fetch recruiters: ${response.status}`);
  }
  return response.json();
}
