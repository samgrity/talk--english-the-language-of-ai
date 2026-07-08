"use client";

import { useState, useEffect } from 'react';
import { getRecruiters } from '@/lib/api';
import { Recruiter } from '@/types/api';

interface RecruiterSelectorProps {
  currentAssigneeId?: string;
  onAssigneeChange: (assigneeId: string | undefined) => void;
  hasChanges: boolean;
  onSave: () => Promise<void>;
}

export default function RecruiterSelector({ 
  currentAssigneeId, 
  onAssigneeChange, 
  hasChanges, 
  onSave 
}: RecruiterSelectorProps) {
  const [recruiters, setRecruiters] = useState<Recruiter[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadRecruiters = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getRecruiters();
        setRecruiters(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load recruiters');
      } finally {
        setLoading(false);
      }
    };

    loadRecruiters();
  }, []);

  const handleAssigneeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    onAssigneeChange(value === '' ? undefined : value);
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      await onSave();
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center gap-3">
        <div className="animate-pulse h-8 bg-gray-200 rounded w-32"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-600 text-sm">
        Error loading recruiters
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <label htmlFor="assignee-select" className="text-sm font-medium text-gray-700">
        Assignee:
      </label>
      <select
        id="assignee-select"
        value={currentAssigneeId || ''}
        onChange={handleAssigneeChange}
        className="rounded-md border border-gray-300 bg-white px-3 py-1.5 text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500"
      >
        <option value="">Unassigned</option>
        {recruiters.map((recruiter) => (
          <option key={recruiter.id} value={recruiter.id}>
            {recruiter.name}
          </option>
        ))}
      </select>
      
      {hasChanges && (
        <button
          onClick={handleSave}
          disabled={saving}
          className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {saving ? 'Saving...' : 'Save'}
        </button>
      )}
    </div>
  );
}
