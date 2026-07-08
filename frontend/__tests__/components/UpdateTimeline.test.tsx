import { render, screen, fireEvent } from '@testing-library/react';
import UpdateTimeline from '@/components/UpdateTimeline';
import { Update } from '@/types/api';

const mockUpdates: Update[] = [
  {
    id: 'update-1',
    timestamp: '2026-03-27T10:00:00Z',
    actor: 'ai_agent',
    internal_notes: 'AI analysis completed. Recommendation: advance.',
    update_type: 'recommend_advance',
    recruiter_id: null,
    correspondence: null,
  },
  {
    id: 'update-2', 
    timestamp: '2026-03-27T11:00:00Z',
    actor: 'human_recruiter',
    internal_notes: 'Reviewed application. All criteria met.',
    update_type: 'advance',
    recruiter_id: 'recruiter-123',
    correspondence: 'Your application has been approved.',
  },
  {
    id: 'update-3',
    timestamp: '2026-03-27T09:00:00Z',
    actor: 'candidate',
    internal_notes: '',
    update_type: 'general_update',
    recruiter_id: null,
    correspondence: 'Thank you for reviewing my application.',
  },
];

describe('UpdateTimeline', () => {
  it('should render updates in chronological order (oldest first)', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    const updateElements = screen.getAllByText(/AI Agent|Recruiter|Candidate/);
    
    // Should be ordered: candidate (09:00), ai_agent (10:00), human_recruiter (11:00)
    expect(updateElements[0]).toHaveTextContent('Candidate');
    expect(updateElements[1]).toHaveTextContent('AI Agent');
    expect(updateElements[2]).toHaveTextContent('Recruiter');
  });

  it('should display correct actor labels', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    expect(screen.getByText('AI Agent')).toBeInTheDocument();
    expect(screen.getByText('Recruiter')).toBeInTheDocument();
    expect(screen.getByText('Candidate')).toBeInTheDocument();
  });

  it('should display correct update type labels', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    expect(screen.getByText('Recommend Advance')).toBeInTheDocument();
    expect(screen.getByText('Advanced')).toBeInTheDocument();

    const generalUpdateBadges = screen.getAllByText('General Update').filter(
      element => element.closest('.px-2.py-1')
    );
    expect(generalUpdateBadges.length).toBeGreaterThan(0);
  });

  it('should show/hide AI updates when toggled', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    // Initially should show all updates including AI
    expect(screen.getByText('AI Agent')).toBeInTheDocument();
    expect(screen.getByText('3 updates')).toBeInTheDocument();

    // Click to hide AI updates
    fireEvent.click(screen.getByText('Hide AI Updates'));

    // Should now show only non-AI updates
    expect(screen.queryByText('AI Agent')).not.toBeInTheDocument();
    expect(screen.getByText('2 updates')).toBeInTheDocument();

    // Click to show AI updates again
    fireEvent.click(screen.getByText('Show AI Updates'));
    expect(screen.getByText('AI Agent')).toBeInTheDocument();
  });

  it('should display both internal notes and correspondence correctly', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    expect(screen.getByDisplayValue('AI analysis completed. Recommendation: advance.')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Your application has been approved.')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Thank you for reviewing my application.')).toBeInTheDocument();
  });

  it('shows recruiter name when recruiter map has an entry', () => {
    render(
      <UpdateTimeline
        updates={mockUpdates}
        reviewerNameMap={{ 'recruiter-123': 'Josh Carter' }}
      />
    );

    expect(screen.getByText('Recruiter: Josh Carter')).toBeInTheDocument();
  });

  it('opens a modal with full text when a read-only text box is clicked', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    fireEvent.click(screen.getByDisplayValue('Your application has been approved.'));

    expect(screen.getByRole('heading', { name: 'Correspondence' })).toBeInTheDocument();
    expect(screen.getByLabelText('Correspondence full text')).toHaveValue(
      'Your application has been approved.'
    );

    fireEvent.click(screen.getByRole('button', { name: 'Done' }));
    expect(screen.queryByLabelText('Correspondence full text')).not.toBeInTheDocument();
  });

  it('closes the modal when escape is pressed', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    fireEvent.click(screen.getByDisplayValue('AI analysis completed. Recommendation: advance.'));
    expect(screen.getByLabelText('Internal Notes full text')).toBeInTheDocument();

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(screen.queryByLabelText('Internal Notes full text')).not.toBeInTheDocument();
  });

  it('omits note/correspondence sections when values are missing', () => {
    const updateWithoutText: Update = {
      id: 'update-no-text',
      timestamp: '2026-03-27T12:00:00Z',
      actor: 'human_recruiter',
      internal_notes: '',
      update_type: 'general_update',
      recruiter_id: null,
      correspondence: '',
    };

    render(<UpdateTimeline updates={[updateWithoutText]} />);

    expect(screen.queryByText('Internal Notes')).not.toBeInTheDocument();
    expect(screen.queryByText('Correspondence')).not.toBeInTheDocument();
  });

  it('sizes preview text boxes by content with a cap of seven rows', () => {
    const longLineUpdate: Update = {
      id: 'update-long-line',
      timestamp: '2026-03-27T13:00:00Z',
      actor: 'human_recruiter',
      internal_notes: 'A'.repeat(800),
      update_type: 'general_update',
      recruiter_id: null,
      correspondence: null,
    };

    render(<UpdateTimeline updates={[longLineUpdate]} />);

    const notePreview = screen.getByLabelText('Internal Notes (read only)') as HTMLTextAreaElement;
    expect(notePreview.rows).toBe(7);
  });

  it('should handle empty updates array', () => {
    render(<UpdateTimeline updates={[]} />);

    expect(screen.getByText('No updates to display')).toBeInTheDocument();
  });

  it('shows toggle button even when all updates are filtered out', () => {
    const aiOnlyUpdates: Update[] = [
      {
        id: 'update-ai-only',
        timestamp: '2026-03-27T10:00:00Z',
        actor: 'ai_agent',
        internal_notes: 'AI note',
        update_type: 'recommend_advance',
        recruiter_id: null,
        correspondence: null,
      },
    ];

    render(<UpdateTimeline updates={aiOnlyUpdates} />);

    fireEvent.click(screen.getByText('Hide AI Updates'));

    expect(screen.getByText('No updates to display')).toBeInTheDocument();
    expect(screen.getByText('Show AI Updates')).toBeInTheDocument();
  });

  it('displays remaining update type labels correctly', () => {
    const miscUpdates: Update[] = [
      {
        id: 'u1',
        timestamp: '2026-03-27T10:00:00Z',
        actor: 'human_recruiter',
        internal_notes: '',
        update_type: 'decline',
        recruiter_id: null,
        correspondence: null,
      },
      {
        id: 'u2',
        timestamp: '2026-03-27T11:00:00Z',
        actor: 'human_recruiter',
        internal_notes: '',
        update_type: 'follow_up',
        recruiter_id: null,
        correspondence: 'Please send docs',
      },
      {
        id: 'u3',
        timestamp: '2026-03-27T12:00:00Z',
        actor: 'human_recruiter',
        internal_notes: '',
        update_type: 'request_ai_screen',
        recruiter_id: null,
        correspondence: null,
      },
      {
        id: 'u4',
        timestamp: '2026-03-27T13:00:00Z',
        actor: 'ai_agent',
        internal_notes: '',
        update_type: 'recommend_decline',
        recruiter_id: null,
        correspondence: null,
      },
      {
        id: 'u5',
        timestamp: '2026-03-27T14:00:00Z',
        actor: 'ai_agent',
        internal_notes: '',
        update_type: 'recommend_follow_up',
        recruiter_id: null,
        correspondence: null,
      },
    ];

    render(<UpdateTimeline updates={miscUpdates} />);

    expect(screen.getByText('Declined')).toBeInTheDocument();
    expect(screen.getByText('Follow-Up')).toBeInTheDocument();
    expect(screen.getByText('Request AI Screen')).toBeInTheDocument();
    expect(screen.getByText('Recommend Decline')).toBeInTheDocument();
    expect(screen.getByText('Recommend Follow-Up')).toBeInTheDocument();
  });

  it('falls back to raw recruiter_id when not in the name map', () => {
    const updateWithUnknownRecruiter: Update[] = [
      {
        id: 'u-unknown',
        timestamp: '2026-03-27T10:00:00Z',
        actor: 'human_recruiter',
        internal_notes: 'Some note',
        update_type: 'general_update',
        recruiter_id: 'rev-unknown-42',
        correspondence: null,
      },
    ];

    render(<UpdateTimeline updates={updateWithUnknownRecruiter} reviewerNameMap={{}} />);

    expect(screen.getByText('Recruiter: rev-unknown-42')).toBeInTheDocument();
  });

  it('does not open modal when read-only text box is empty or whitespace', () => {
    const updateWithWhitespace: Update[] = [
      {
        id: 'u-ws',
        timestamp: '2026-03-27T10:00:00Z',
        actor: 'human_recruiter',
        internal_notes: '   ',
        update_type: 'general_update',
        recruiter_id: null,
        correspondence: null,
      },
    ];

    render(<UpdateTimeline updates={updateWithWhitespace} />);
    expect(screen.queryByLabelText('Internal Notes (read only)')).not.toBeInTheDocument();
  });

  it('should apply correct styling for different actors', () => {
    render(<UpdateTimeline updates={mockUpdates} />);

    const aiUpdate = screen.getByText('AI Agent').closest('.border');
    const humanUpdate = screen.getByText('Recruiter').closest('.border');
    const candidateUpdate = screen.getByText('Candidate').closest('.border');

    expect(aiUpdate).toHaveClass('text-blue-800');
    expect(humanUpdate).toHaveClass('text-green-800'); 
    expect(candidateUpdate).toHaveClass('text-purple-800');
  });
});
