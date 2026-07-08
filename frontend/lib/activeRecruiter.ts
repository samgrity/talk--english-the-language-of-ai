import { Recruiter } from '@/types/api';

export interface ActiveRecruiter {
  id: string;
  name: string;
}

const STORAGE_KEY = 'hireflow.active_recruiter';

export function getActiveRecruiter(): ActiveRecruiter | null {
  if (typeof window === 'undefined') {
    return null;
  }

  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    const parsed = JSON.parse(raw) as ActiveRecruiter;
    if (!parsed.id || !parsed.name) {
      return null;
    }
    return parsed;
  } catch {
    return null;
  }
}

export function setActiveRecruiter(recruiter: Recruiter): void {
  if (typeof window === 'undefined') {
    return;
  }

  const payload: ActiveRecruiter = {
    id: recruiter.id,
    name: recruiter.name,
  };
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export function clearActiveRecruiter(): void {
  if (typeof window === 'undefined') {
    return;
  }

  window.localStorage.removeItem(STORAGE_KEY);
}
