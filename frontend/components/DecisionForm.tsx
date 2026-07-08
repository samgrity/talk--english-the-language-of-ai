import { useState } from 'react';
import { NewUpdateRequest, Update } from '@/types/api';

interface Props {
  onSubmit: (update: NewUpdateRequest) => Promise<void>;
  disabled?: boolean;
  latestUpdate?: Update;
}

const UPDATE_TYPE_OPTIONS = [
  { value: 'advance', label: 'Advance Candidate', color: 'text-green-700' },
  { value: 'decline', label: 'Decline Candidate', color: 'text-red-700' },
  { value: 'withdraw', label: 'Withdraw Application', color: 'text-gray-700' },
  { value: 'follow_up', label: 'Follow Up', color: 'text-yellow-700' },
  { value: 'request_ai_screen', label: 'Request AI Screen', color: 'text-indigo-700' },
  { value: 'general_update', label: 'General Update', color: 'text-blue-700' },
];

export default function DecisionForm({ onSubmit, disabled = false, latestUpdate }: Props) {
  const [updateType, setUpdateType] = useState<string>('');
  const [internalNotes, setInternalNotes] = useState<string>('');
  const [correspondence, setCorrespondence] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!updateType) {
      newErrors.updateType = 'Please select an update type';
    }

    if (updateType === 'follow_up' && !correspondence.trim()) {
      newErrors.correspondence = 'Correspondence is required for this update type';
    }

    if (internalNotes.length > 2000) {
      newErrors.internalNotes = 'Internal notes must be 2000 characters or less';
    }

    if (correspondence.length > 2000) {
      newErrors.correspondence = 'Correspondence must be 2000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const trimmedCorrespondence = correspondence.trim();
      const updateData: NewUpdateRequest = {
        update_type: updateType,
        internal_notes: internalNotes.trim() || '',
        correspondence: trimmedCorrespondence || undefined,
      };

      await onSubmit(updateData);

      setUpdateType('');
      setInternalNotes('');
      setCorrespondence('');
    } catch (error) {
      setErrors({
        submit: error instanceof Error ? error.message : 'Failed to submit update'
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCopyAIRecommendation = () => {
    if (!latestUpdate || latestUpdate.actor !== 'ai_agent') return;
    
    let humanUpdateType = '';
    switch (latestUpdate.update_type) {
      case 'recommend_advance':
        humanUpdateType = 'advance';
        break;
      case 'recommend_decline':
        humanUpdateType = 'decline';
        break;
      case 'recommend_follow_up':
        humanUpdateType = 'follow_up';
        break;
      default:
        return;
    }
    
    setUpdateType(humanUpdateType);
    setCorrespondence(latestUpdate.correspondence || '');
  };

  const canCopyAIRecommendation = latestUpdate &&
    latestUpdate.actor === 'ai_agent' && 
    ['recommend_advance', 'recommend_decline', 'recommend_follow_up'].includes(latestUpdate.update_type);

  const selectedOption = UPDATE_TYPE_OPTIONS.find(opt => opt.value === updateType);
  const followUpWithoutCorrespondence = updateType === 'follow_up' && !correspondence.trim();
  const showCorrespondenceField = updateType === 'follow_up' || correspondence.trim().length > 0;

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-gray-900">Add New Update</h3>
          {canCopyAIRecommendation && (
            <button
              type="button"
              onClick={handleCopyAIRecommendation}
              disabled={disabled || isSubmitting}
              className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:text-gray-500"
            >
              Copy AI Recommendation
            </button>
          )}
        </div>

        <div className="mb-4">
          <label htmlFor="updateType" className="block text-sm font-medium text-gray-700 mb-2">
            Update Type <span className="text-red-500">*</span>
          </label>
          <select
            id="updateType"
            value={updateType}
            onChange={(e) => {
              const nextUpdateType = e.target.value;
              setUpdateType(nextUpdateType);
              if (nextUpdateType !== 'follow_up') {
                setCorrespondence('');
              }
            }}
            disabled={disabled || isSubmitting}
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              errors.updateType ? 'border-red-500' : 'border-gray-300'
            } ${disabled || isSubmitting ? 'bg-gray-100 cursor-not-allowed' : ''}`}
          >
            <option value="">Select update type...</option>
            {UPDATE_TYPE_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {errors.updateType && (
            <p className="mt-1 text-sm text-red-600">{errors.updateType}</p>
          )}
          {selectedOption && (
            <p className={`mt-1 text-sm ${selectedOption.color}`}>
              {getUpdateTypeDescription(updateType)}
            </p>
          )}
        </div>

        <div className="mb-4">
          <label htmlFor="internalNotes" className="block text-sm font-medium text-gray-700 mb-2">
            Internal Notes
          </label>
          <textarea
            id="internalNotes"
            value={internalNotes}
            onChange={(e) => setInternalNotes(e.target.value)}
            disabled={disabled || isSubmitting}
            rows={4}
            maxLength={2000}
            placeholder="Enter your internal notes about this candidate..."
            className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical ${
              errors.internalNotes ? 'border-red-500' : 'border-gray-300'
            } ${disabled || isSubmitting ? 'bg-gray-100 cursor-not-allowed' : ''}`}
          />
          <div className="flex justify-between items-start mt-1">
            <div>
              {errors.internalNotes && (
                <p className="text-sm text-red-600">{errors.internalNotes}</p>
              )}
            </div>
            <p className="text-xs text-gray-500">{internalNotes.length}/2000</p>
          </div>
        </div>

        {showCorrespondenceField && (
          <div className="mb-6">
            <label htmlFor="correspondence" className="block text-sm font-medium text-gray-700 mb-2">
              Correspondence to Candidate
              {updateType === 'follow_up' && <span className="text-red-500"> *</span>}
            </label>
            <textarea
              id="correspondence"
              value={correspondence}
              onChange={(e) => setCorrespondence(e.target.value)}
              disabled={disabled || isSubmitting}
              rows={3}
              maxLength={2000}
              placeholder="Enter the message requesting additional information from the candidate..."
              className={`w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-vertical ${
                errors.correspondence ? 'border-red-500' : 'border-gray-300'
              } ${disabled || isSubmitting ? 'bg-gray-100 cursor-not-allowed' : ''}`}
            />
            {updateType !== 'follow_up' && correspondence.trim().length > 0 && (
              <p className="mt-1 text-xs text-gray-500">
                Copied from AI recommendation. This message will be submitted with this update.
              </p>
            )}
            <div className="flex justify-between items-start mt-1">
              <div>
                {errors.correspondence && (
                  <p className="text-sm text-red-600">{errors.correspondence}</p>
                )}
              </div>
              <p className="text-xs text-gray-500">{correspondence.length}/2000</p>
            </div>
          </div>
        )}

        {errors.submit && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{errors.submit}</p>
          </div>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={disabled || isSubmitting || !updateType || followUpWithoutCorrespondence}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              disabled || isSubmitting || !updateType || followUpWithoutCorrespondence
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2'
            }`}
          >
            {isSubmitting ? 'Submitting...' : 'Submit Update'}
          </button>
        </div>
      </div>
    </form>
  );
}

function getUpdateTypeDescription(updateType: string): string {
  switch (updateType) {
    case 'advance':
      return 'This will advance the candidate to the next stage.';
    case 'decline':
      return 'This will decline the candidate\'s application.';
    case 'withdraw':
      return 'This will mark the application as withdrawn and remove it from the active pipeline.';
    case 'follow_up':
      return 'This will request additional information from the candidate.';
    case 'request_ai_screen':
      return 'This will log your notes, set the application to waiting for AI, and immediately trigger a new AI screening.';
    case 'general_update':
      return 'This will add a general recruiter update and optional candidate-facing correspondence.';
    default:
      return '';
  }
}
