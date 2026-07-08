import { useState } from 'react';
import TextPreviewModal from './TextPreviewModal';
import { Update } from '@/types/api';

interface Props {
  updates: Update[];
  reviewerNameMap?: Record<string, string>;
}

export default function UpdateTimeline({ updates, reviewerNameMap = {} }: Props) {
  const [showAiUpdates, setShowAiUpdates] = useState(true);
  const [modalContent, setModalContent] = useState<{
    title: string;
    text: string;
  } | null>(null);

  const sortedUpdates = [...updates].sort((a, b) => 
    new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
  );

  const filteredUpdates = sortedUpdates.filter(update => 
    showAiUpdates || update.actor !== 'ai_agent'
  );

  const estimateRows = (text: string, maxCharsPerLine: number, maxRows: number) => {
    const lineCount = text.split('\n').reduce((total, line) => {
      const estimatedWrapped = Math.ceil(Math.max(line.length, 1) / maxCharsPerLine);
      return total + Math.max(estimatedWrapped, 1);
    }, 0);

    return Math.max(1, Math.min(lineCount, maxRows));
  };

  const getActorColor = (actor: string) => {
    switch (actor) {
      case 'ai_agent':
        return 'bg-blue-50 border-blue-200 text-blue-800';
      case 'human_recruiter':
        return 'bg-green-50 border-green-200 text-green-800';
      case 'candidate':
        return 'bg-purple-50 border-purple-200 text-purple-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getActorLabel = (actor: string) => {
    switch (actor) {
      case 'ai_agent':
        return 'AI Agent';
      case 'human_recruiter':
        return 'Recruiter';
      case 'candidate':
        return 'Candidate';
      default:
        return actor;
    }
  };

  const getUpdateTypeLabel = (updateType: string) => {
    switch (updateType) {
      case 'recommend_advance':
        return 'Recommend Advance';
      case 'recommend_decline':
        return 'Recommend Decline';
      case 'recommend_follow_up':
        return 'Recommend Follow-Up';
      case 'advance':
        return 'Advanced';
      case 'decline':
        return 'Declined';
      case 'follow_up':
        return 'Follow-Up';
      case 'request_ai_screen':
        return 'Request AI Screen';
      case 'general_update':
        return 'General Update';
      default:
        return updateType;
    }
  };

  const openTextModal = (title: string, text: string) => {
    if (!text.trim()) {
      return;
    }
    setModalContent({ title, text });
  };

  const renderReadonlyTextBox = (
    sectionTitle: string,
    content: string | null | undefined
  ) => {
    if (!content || !content.trim()) {
      return null;
    }

    return (
      <div className="mb-3">
        <label className="block text-xs font-medium text-current/70 mb-1">
          {sectionTitle}
        </label>
        <textarea
          readOnly
          rows={estimateRows(content, 62, 7)}
          value={content}
          onClick={() => openTextModal(sectionTitle, content)}
          wrap="soft"
          className="w-full rounded-md border border-current/20 bg-white/80 p-2 text-sm leading-5 text-gray-900 overflow-y-auto resize-none cursor-pointer"
          aria-label={`${sectionTitle} (read only)`}
        />
      </div>
    );
  };

  if (filteredUpdates.length === 0) {
    return (
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">No updates to display</span>
          <button
            onClick={() => setShowAiUpdates(!showAiUpdates)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {showAiUpdates ? 'Hide' : 'Show'} AI Updates
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between border-b border-gray-200 pb-3">
        <span className="text-sm text-gray-600">
          {filteredUpdates.length} update{filteredUpdates.length !== 1 ? 's' : ''}
        </span>
        <button
          onClick={() => setShowAiUpdates(!showAiUpdates)}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          {showAiUpdates ? 'Hide' : 'Show'} AI Updates
        </button>
      </div>

      <div className="space-y-4">
        {filteredUpdates.map((update) => {
          const recruiterLabel = update.recruiter_id
            ? reviewerNameMap[update.recruiter_id] || update.recruiter_id
            : null;

          return (
            <div key={update.id} className="relative">
              <div className={`border rounded-lg p-4 ${getActorColor(update.actor)}`}>
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 rounded-full bg-current"></div>
                    <span className="font-medium text-sm">
                      {getActorLabel(update.actor)}
                    </span>
                    <span className="px-2 py-1 bg-white/50 rounded text-xs">
                      {getUpdateTypeLabel(update.update_type)}
                    </span>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-current/70">
                      {new Date(update.timestamp).toLocaleDateString()} at{' '}
                      {new Date(update.timestamp).toLocaleTimeString([], { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </p>
                    {recruiterLabel && (
                      <p className="text-xs text-current/70">
                        Recruiter: {recruiterLabel}
                      </p>
                    )}
                  </div>
                </div>

                {renderReadonlyTextBox('Internal Notes', update.internal_notes)}
                {renderReadonlyTextBox('Correspondence', update.correspondence)}
              </div>
            </div>
          );
        })}
      </div>

      {modalContent && (
        <TextPreviewModal
          title={modalContent.title}
          text={modalContent.text}
          onDone={() => setModalContent(null)}
        />
      )}
    </div>
  );
}
