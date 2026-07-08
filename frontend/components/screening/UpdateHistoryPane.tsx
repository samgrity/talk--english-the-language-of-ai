import { useEffect, useState } from 'react';
import DecisionForm from '@/components/DecisionForm';
import UpdateTimeline from '@/components/UpdateTimeline';
import { getRecruiters } from '@/lib/api';
import { NewUpdateRequest, Update } from '@/types/api';

interface Props {
  updates: Update[];
  submittingUpdate: boolean;
  onSubmitUpdate: (update: NewUpdateRequest) => Promise<void>;
}

export default function UpdateHistoryPane({
  updates,
  submittingUpdate,
  onSubmitUpdate,
}: Props) {
  const [reviewerNameMap, setReviewerNameMap] = useState<Record<string, string>>({});

  useEffect(() => {
    let cancelled = false;

    const loadRecruiters = async () => {
      try {
        const recruiters = await getRecruiters();
        if (cancelled) {
          return;
        }

        const nextMap = recruiters.reduce<Record<string, string>>((acc, recruiter) => {
          acc[recruiter.id] = recruiter.name;
          return acc;
        }, {});
        setReviewerNameMap(nextMap);
      } catch {
        if (!cancelled) {
          setReviewerNameMap({});
        }
      }
    };

    void loadRecruiters();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="flex-1 bg-white rounded-lg shadow overflow-y-auto">
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Activity Timeline</h2>

        <div className="mb-6">
          <UpdateTimeline updates={updates} reviewerNameMap={reviewerNameMap} />
        </div>

        <div className="border-t pt-4">
          <DecisionForm
            onSubmit={onSubmitUpdate}
            disabled={submittingUpdate}
            latestUpdate={updates.length > 0 ? updates[updates.length - 1] : undefined}
          />
        </div>
      </div>
    </div>
  );
}
