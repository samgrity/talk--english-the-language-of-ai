"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import ActiveRecruiterBadge from '@/components/ActiveRecruiterBadge';
import CandidateDetailsPane from '@/components/screening/CandidateDetailsPane';
import UpdateHistoryPane from '@/components/screening/UpdateHistoryPane';
import RecruiterSelector from '@/components/screening/RecruiterSelector';
import { ActiveRecruiter, getActiveRecruiter } from '@/lib/activeRecruiter';
import { useScreenCandidate } from '@/hooks/useScreenCandidate';

export default function ScreenPage() {
  const params = useParams();
  const router = useRouter();
  const id = typeof params.id === 'string' ? params.id : null;
  const [activeRecruiter, setActiveRecruiter] = useState<ActiveRecruiter | null>(null);
  const [authChecked, setAuthChecked] = useState(false);

  useEffect(() => {
    const reviewer = getActiveRecruiter();
    if (!reviewer) {
      router.replace('/login');
      return;
    }
    setActiveRecruiter(reviewer);
    setAuthChecked(true);
  }, [router]);

  const {
    application,
    editedApplication,
    loading,
    error,
    hasChanges,
    submittingUpdate,
    loadApplication,
    updateFirstName,
    updateLastName,
    updateField,
    updateCompanyField,
    addSubDepartment,
    removeSubDepartment,
    updateAssignee,
    saveApplication,
    submitUpdate,
  } = useScreenCandidate(id, activeRecruiter?.id ?? null);

  if (!authChecked || loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-2">
        <div className="w-full">
          <div className="animate-pulse">
            <div className="h-6 bg-gray-200 rounded w-64 mb-4" />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-white rounded-lg shadow p-6 h-96" />
              <div className="bg-white rounded-lg shadow p-6 h-96" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-2">
        <div className="w-full">
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <p className="text-red-800">Error: {error}</p>
            <button
              onClick={() => {
                void loadApplication();
              }}
              className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!application || !editedApplication) {
    return (
      <div className="min-h-screen bg-gray-50 p-2">
        <div className="w-full">
          <p className="text-gray-600">Candidate not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="w-full p-2">
        <nav className="mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm min-w-0">
              <Link href="/queue" className="text-blue-600 hover:text-blue-800">
                Candidate Pipeline
              </Link>
              <span className="text-gray-500">/</span>
              <span className="text-gray-900 truncate">
                {application.firstName} {application.lastName}
              </span>
            </div>
            <div className="flex items-center gap-3">
              {activeRecruiter && <ActiveRecruiterBadge recruiter={activeRecruiter} />}
              <RecruiterSelector
                currentAssigneeId={editedApplication.assignee_id}
                onAssigneeChange={updateAssignee}
                hasChanges={hasChanges}
                onSave={saveApplication}
              />
            </div>
          </div>
        </nav>

        <div className="flex flex-col xl:flex-row gap-4 h-[calc(100vh-84px)]">
          <CandidateDetailsPane
            application={editedApplication}
            hasChanges={hasChanges}
            onFirstNameChange={updateFirstName}
            onLastNameChange={updateLastName}
            onFieldChange={updateField}
            onCompanyFieldChange={updateCompanyField}
            onSubDepartmentAdd={addSubDepartment}
            onSubDepartmentRemove={removeSubDepartment}
            onSave={saveApplication}
          />

          <UpdateHistoryPane
            updates={application.updates}
            submittingUpdate={submittingUpdate}
            onSubmitUpdate={submitUpdate}
          />
        </div>
      </div>
    </div>
  );
}
