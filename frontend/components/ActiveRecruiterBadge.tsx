"use client";

import { ActiveRecruiter } from '@/lib/activeRecruiter';

interface ActiveRecruiterBadgeProps {
  recruiter: ActiveRecruiter;
}

export default function ActiveRecruiterBadge({ recruiter }: ActiveRecruiterBadgeProps) {
  return (
    <div className="flex items-center gap-2 rounded-md border border-gray-200 bg-white px-3 py-1.5 text-sm">
      <span className="text-gray-500">Active Recruiter:</span>
      <span className="font-medium text-gray-900">{recruiter.name}</span>
    </div>
  );
}
