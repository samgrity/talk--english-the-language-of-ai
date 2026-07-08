"use client";

import { useState, useEffect, useCallback, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import ActiveRecruiterBadge from '@/components/ActiveRecruiterBadge';
import { ActiveRecruiter, getActiveRecruiter } from '@/lib/activeRecruiter';
import { ApplicationSummary, FilterStatus, Recruiter } from '@/types/api';
import { getApplications, getRecruiters } from '@/lib/api';
import CandidateTable from '@/components/CandidateTable';

function QueuePageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [applications, setApplications] = useState<ApplicationSummary[]>([]);
  const [recruiters, setRecruiters] = useState<Recruiter[]>([]);
  const [activeRecruiter, setActiveRecruiter] = useState<ActiveRecruiter | null>(null);
  const [authChecked, setAuthChecked] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isFiltering, setIsFiltering] = useState(false);
  
  const [searchText, setSearchText] = useState<string>(searchParams.get('search') || '');
  const [statusFilter, setStatusFilter] = useState<string>(
    searchParams.get('filter') || FilterStatus.PENDING
  );
  const [assigneeFilter, setAssigneeFilter] = useState<string>(
    searchParams.get('assignee_id') || ''
  );

  const updateURL = useCallback((filter: string, search: string, assigneeId: string) => {
    const params = new URLSearchParams();
    params.set('filter', filter || FilterStatus.PENDING);
    params.set('search', search);
    params.set('assignee_id', assigneeId || 'all');
    
    const newURL = params.toString() ? `?${params.toString()}` : '/queue';
    router.replace(newURL, { scroll: false });
  }, [router]);

  useEffect(() => {
    const reviewer = getActiveRecruiter();
    if (!reviewer) {
      router.replace('/login');
      return;
    }

    const initialAssigneeFilter = searchParams.get('assignee_id') || reviewer.id;
    setAssigneeFilter(initialAssigneeFilter);
    updateURL(statusFilter, searchText, initialAssigneeFilter);

    setActiveRecruiter(reviewer);
    setAuthChecked(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [router, updateURL]);

  const loadApplications = useCallback(async (filter?: string, search?: string, assigneeId?: string) => {
    try {
      if (loading) {
        setLoading(true);
      } else {
        setIsFiltering(true);
      }
      setError(null);
      const resolvedAssignee = assigneeId ?? assigneeFilter;
      const data = await getApplications(
        filter || statusFilter,
        search || searchText,
        resolvedAssignee === 'all' ? undefined : resolvedAssignee
      );
      setApplications(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load applications');
    } finally {
      setLoading(false);
      setIsFiltering(false);
    }
  }, [assigneeFilter, loading, statusFilter, searchText]);

  const loadRecruiters = useCallback(async () => {
    try {
      const data = await getRecruiters();
      setRecruiters(data);
    } catch {
      setRecruiters([]);
    }
  }, []);

  useEffect(() => {
    if (!authChecked) {
      return;
    }
    loadRecruiters();
    loadApplications();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [authChecked]);

  useEffect(() => {
    if (authChecked && !loading) {
      updateURL(statusFilter, searchText, assigneeFilter);
      loadApplications(statusFilter, searchText, assigneeFilter);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [statusFilter]);

  useEffect(() => {
    if (authChecked && !loading) {
      const timer = setTimeout(() => {
        updateURL(statusFilter, searchText, assigneeFilter);
        loadApplications(statusFilter, searchText, assigneeFilter);
      }, 1000);

      return () => clearTimeout(timer);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchText]);

  useEffect(() => {
    if (authChecked && !loading) {
      updateURL(statusFilter, searchText, assigneeFilter);
      loadApplications(statusFilter, searchText, assigneeFilter);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [assigneeFilter]);

  if (!authChecked || loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Candidate Pipeline</h1>
          <div className="animate-pulse">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-6 py-3 border-b border-gray-200">
                <div className="h-4 bg-gray-300 rounded w-1/4"></div>
              </div>
              {[1, 2, 3].map(i => (
                <div key={i} className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center space-x-4">
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/4"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/5"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/12"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Candidate Pipeline</h1>
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">Error: {error}</p>
            <button
              onClick={() => loadApplications()}
              className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto px-6 py-6">
        <div className="mb-8">
          <div className="flex items-center justify-between gap-4 mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Candidate Pipeline</h1>
            {activeRecruiter && <ActiveRecruiterBadge recruiter={activeRecruiter} />}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4 mb-6">
          {isFiltering && (
            <div className="mb-3 flex items-center text-sm text-blue-600">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              Filtering candidates...
            </div>
          )}
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
                Search Candidates
              </label>
              <input
                id="search"
                type="text"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
                placeholder="Search across all fields..."
                autoComplete="off"
                autoCapitalize="off"
                autoCorrect="off"
                spellCheck="false"
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="sm:w-64">
              <label htmlFor="status-filter" className="block text-sm font-medium text-gray-700 mb-1">
                Screening Status
              </label>
              <select
                id="status-filter"
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value={FilterStatus.PENDING}>Pending</option>
                <option value={FilterStatus.COMPLETED}>Completed</option>
                <option value={FilterStatus.ALL}>All Statuses</option>
                <optgroup label="Specific Statuses">
                  <option value={FilterStatus.WAITING_FOR_RECRUITER}>Waiting for Recruiter</option>
                  <option value={FilterStatus.WAITING_FOR_AI}>Waiting for AI</option>
                  <option value={FilterStatus.WAITING_FOR_CANDIDATE}>Waiting for Candidate</option>
                  <option value={FilterStatus.ADVANCED}>Advanced</option>
                  <option value={FilterStatus.DECLINED}>Declined</option>
                  <option value={FilterStatus.WITHDRAWN}>Withdrawn</option>
                </optgroup>
              </select>
            </div>

            <div className="sm:w-64">
              <label htmlFor="assignee-filter" className="block text-sm font-medium text-gray-700 mb-1">
                Assignee
              </label>
              <select
                id="assignee-filter"
                value={assigneeFilter}
                onChange={(e) => setAssigneeFilter(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="all">All assignees</option>
                {recruiters.map((recruiter) => (
                  <option key={recruiter.id} value={recruiter.id}>
                    {recruiter.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {applications.length === 0 ? (
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="text-center py-12">
              <p className="text-gray-500">No candidates found for this filter.</p>
            </div>
          </div>
        ) : (
          <CandidateTable applications={applications} />
        )}
      </div>
    </div>
  );
}

export default function QueuePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Candidate Pipeline</h1>
          <div className="animate-pulse">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <div className="px-6 py-3 border-b border-gray-200">
                <div className="h-4 bg-gray-300 rounded w-1/4"></div>
              </div>
              {[1, 2, 3].map(i => (
                <div key={i} className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center space-x-4">
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/4"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/5"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/6"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/12"></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    }>
      <QueuePageContent />
    </Suspense>
  );
}
