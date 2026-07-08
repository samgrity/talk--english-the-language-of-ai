import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DecisionForm from '@/components/DecisionForm';
import { NewUpdateRequest, Update } from '@/types/api';

describe('DecisionForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('should render form elements correctly', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    expect(screen.getByText('Add New Update')).toBeInTheDocument();
    expect(screen.getByLabelText(/Update Type/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Internal Notes/)).toBeInTheDocument();
    expect(screen.queryByLabelText(/Correspondence to Candidate/)).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Submit Update' })).toBeInTheDocument();
  });

  it('should show all update type options', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const select = screen.getByLabelText(/Update Type/);
    fireEvent.click(select);

    expect(screen.getByText('Advance Candidate')).toBeInTheDocument();
    expect(screen.getByText('Decline Candidate')).toBeInTheDocument();
    expect(screen.getByText('Withdraw Application')).toBeInTheDocument();
    expect(screen.getByText('Follow Up')).toBeInTheDocument();
    expect(screen.getByText('Request AI Screen')).toBeInTheDocument();
    expect(screen.getByText('General Update')).toBeInTheDocument();
  });

  it('should require only update type', async () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const submitButton = screen.getByRole('button', { name: 'Submit Update' });
    expect(submitButton).toBeDisabled();
  });

  it('should enable submit button when required fields are filled', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/);
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    fireEvent.change(updateTypeSelect, { target: { value: 'general_update' } });
    fireEvent.change(internalNotesTextarea, { target: { value: 'Test internal notes' } });

    expect(submitButton).not.toBeDisabled();
  });

  it('should require correspondence for follow_up update type', async () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    fireEvent.change(updateTypeSelect, { target: { value: 'follow_up' } });

    const correspondenceTextarea = screen.getByLabelText(/Correspondence to Candidate/);
    expect(submitButton).toBeDisabled();

    fireEvent.change(correspondenceTextarea, { target: { value: 'Test correspondence' } });
    expect(submitButton).not.toBeDisabled();
  });

  it('should show character counts', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const characterCounts = screen.getAllByText('0/2000');
    expect(characterCounts.length).toBeGreaterThan(0);
  });

  it('should update character counts when typing', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/);
    fireEvent.change(internalNotesTextarea, { target: { value: 'Test' } });

    expect(screen.getByText('4/2000')).toBeInTheDocument();
  });

  it('should show update type description', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    fireEvent.change(updateTypeSelect, { target: { value: 'advance' } });

    expect(screen.getByText('This will advance the candidate to the next stage.')).toBeInTheDocument();
  });

  it('should call onSubmit with correct data', async () => {
    mockOnSubmit.mockResolvedValueOnce(undefined);
    
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/);
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    fireEvent.change(updateTypeSelect, { target: { value: 'follow_up' } });
    fireEvent.change(internalNotesTextarea, { target: { value: 'Candidate looks good' } });

    const correspondenceTextarea = screen.getByLabelText(/Correspondence to Candidate/);
    fireEvent.change(correspondenceTextarea, { target: { value: 'Welcome to the interview!' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        update_type: 'follow_up',
        internal_notes: 'Candidate looks good',
        correspondence: 'Welcome to the interview!'
      });
    });
  });

  it('should reset form after successful submission', async () => {
    mockOnSubmit.mockResolvedValueOnce(undefined);
    
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/) as HTMLSelectElement;
    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/) as HTMLTextAreaElement;
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    fireEvent.change(updateTypeSelect, { target: { value: 'general_update' } });
    fireEvent.change(internalNotesTextarea, { target: { value: 'Test general update' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(updateTypeSelect.value).toBe('');
      expect(internalNotesTextarea.value).toBe('');
    });
  });

  it('should handle submission errors', async () => {
    mockOnSubmit.mockRejectedValueOnce(new Error('Submission failed'));
    
    render(<DecisionForm onSubmit={mockOnSubmit} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/);
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    fireEvent.change(updateTypeSelect, { target: { value: 'general_update' } });
    fireEvent.change(internalNotesTextarea, { target: { value: 'Test general update' } });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Submission failed')).toBeInTheDocument();
    });
  });

  it('should show copy AI recommendation button when latest update is from AI agent', () => {
    const mockLatestUpdate: Update = {
      id: 'update-1',
      timestamp: '2026-03-27T12:00:00Z',
      actor: 'ai_agent',
      internal_notes: 'Candidate appears legitimate based on verification.',
      update_type: 'recommend_advance',
      correspondence: 'Welcome to HireFlow!'
    };

    render(<DecisionForm onSubmit={mockOnSubmit} latestUpdate={mockLatestUpdate} />);

    expect(screen.getByRole('button', { name: 'Copy AI Recommendation' })).toBeInTheDocument();
  });

  it('should not show copy button when latest update is not from AI agent', () => {
    const mockLatestUpdate: Update = {
      id: 'update-1',
      timestamp: '2026-03-27T12:00:00Z',
      actor: 'human_recruiter',
      internal_notes: 'Looks good to me.',
      update_type: 'advance',
      correspondence: 'Welcome!'
    };

    render(<DecisionForm onSubmit={mockOnSubmit} latestUpdate={mockLatestUpdate} />);

    expect(screen.queryByRole('button', { name: 'Copy AI Recommendation' })).not.toBeInTheDocument();
  });

  it('should copy AI recommendation when button is clicked', () => {
    const mockLatestUpdate: Update = {
      id: 'update-1',
      timestamp: '2026-03-27T12:00:00Z',
      actor: 'ai_agent',
      internal_notes: 'Candidate appears legitimate.',
      update_type: 'recommend_follow_up',
      correspondence: 'Please share one additional project example.'
    };

    render(<DecisionForm onSubmit={mockOnSubmit} latestUpdate={mockLatestUpdate} />);

    const copyButton = screen.getByRole('button', { name: 'Copy AI Recommendation' });
    fireEvent.click(copyButton);

    const updateTypeSelect = screen.getByLabelText(/Update Type/) as HTMLSelectElement;
    const correspondenceTextarea = screen.getByLabelText(/Correspondence to Candidate/) as HTMLTextAreaElement;

    expect(updateTypeSelect.value).toBe('follow_up');
    expect(correspondenceTextarea.value).toBe('Please share one additional project example.');
  });

  it('should be disabled when disabled prop is true', () => {
    render(<DecisionForm onSubmit={mockOnSubmit} disabled={true} />);

    const updateTypeSelect = screen.getByLabelText(/Update Type/);
    const internalNotesTextarea = screen.getByLabelText(/Internal Notes/);
    const submitButton = screen.getByRole('button', { name: 'Submit Update' });

    expect(updateTypeSelect).toBeDisabled();
    expect(internalNotesTextarea).toBeDisabled();
    expect(submitButton).toBeDisabled();
  });
});
