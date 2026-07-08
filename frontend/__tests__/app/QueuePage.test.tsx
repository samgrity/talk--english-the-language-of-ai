import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import QueuePage from '@/app/queue/page';
import { getApplications, getRecruiters } from '@/lib/api';
import { getActiveRecruiter } from '@/lib/activeRecruiter';

const mockReplace = jest.fn();
const mockSearchParamsGet = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({
    replace: mockReplace,
  }),
  useSearchParams: () => ({
    get: mockSearchParamsGet,
  }),
}));

jest.mock('@/lib/activeRecruiter', () => ({
  getActiveRecruiter: jest.fn(),
}));

jest.mock('@/lib/api', () => ({
  getApplications: jest.fn(),
  getRecruiters: jest.fn(),
}));

const mockApplications = [
  {
    id: 'app-1',
    firstName: 'James',
    lastName: 'Walker',
    email: 'james@example.com',
    mobile: '+1-555-0100',
    jobTitle: 'Engineer',
    seniorityLevel: 'Senior',
    department: 'ENGINEERING',
    companyName: 'Acme',
    companySize: 'Large',
    companyType: 'Enterprise',
    region: 'North America/United States',
    screeningStatus: 'waiting_for_recruiter',
    assignee_id: 'rev1',
    assignee_name: 'John Berryman',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-02T00:00:00Z',
  },
];

describe('QueuePage URL filter behavior', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    (getActiveRecruiter as jest.Mock).mockReturnValue({ id: 'rev1', name: 'John Berryman' });
    (getRecruiters as jest.Mock).mockResolvedValue([
      { id: 'rev1', name: 'John Berryman' },
      { id: 'rev2', name: 'Josh Carter' },
    ]);
    (getApplications as jest.Mock).mockResolvedValue([]);
  });

  it('preserves assignee_id=all and does not force active recruiter filter', async () => {
    mockSearchParamsGet.mockImplementation((key: string) => {
      if (key === 'filter') return 'all';
      if (key === 'search') return '';
      if (key === 'assignee_id') return 'all';
      return null;
    });

    render(<QueuePage />);

    await waitFor(() => {
      expect(getApplications).toHaveBeenCalledWith('all', '', undefined);
    });

    expect(screen.getByLabelText('Assignee')).toHaveValue('all');
    expect(mockReplace).toHaveBeenCalledWith(
      expect.stringContaining('assignee_id=all'),
      { scroll: false }
    );
  });

  it('keeps assignee selection explicit in URL when toggling all assignees', async () => {
    mockSearchParamsGet.mockImplementation((key: string) => {
      if (key === 'filter') return 'pending';
      if (key === 'search') return '';
      if (key === 'assignee_id') return 'rev1';
      return null;
    });

    render(<QueuePage />);

    const assigneeSelect = await screen.findByLabelText('Assignee');

    fireEvent.change(assigneeSelect, { target: { value: 'all' } });

    await waitFor(() => {
      expect(mockReplace).toHaveBeenCalledWith(
        expect.stringContaining('assignee_id=all'),
        { scroll: false }
      );
    });
  });
});

describe('QueuePage redirect and error behavior', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockSearchParamsGet.mockReturnValue(null);
  });

  it('redirects to /login when no active recruiter is set', () => {
    (getActiveRecruiter as jest.Mock).mockReturnValue(null);
    (getRecruiters as jest.Mock).mockResolvedValue([]);
    (getApplications as jest.Mock).mockResolvedValue([]);

    render(<QueuePage />);

    expect(mockReplace).toHaveBeenCalledWith('/login');
  });

  it('shows error state and retry button when API call fails', async () => {
    (getActiveRecruiter as jest.Mock).mockReturnValue({ id: 'rev1', name: 'John Berryman' });
    (getRecruiters as jest.Mock).mockResolvedValue([]);
    (getApplications as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText(/Network error/)).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
  });

  it('shows empty state message when no candidates match filters', async () => {
    (getActiveRecruiter as jest.Mock).mockReturnValue({ id: 'rev1', name: 'John Berryman' });
    (getRecruiters as jest.Mock).mockResolvedValue([]);
    (getApplications as jest.Mock).mockResolvedValue([]);

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText('No candidates found for this filter.')).toBeInTheDocument();
    });
  });

  it('renders candidate rows when data is returned', async () => {
    (getActiveRecruiter as jest.Mock).mockReturnValue({ id: 'rev1', name: 'John Berryman' });
    (getRecruiters as jest.Mock).mockResolvedValue([{ id: 'rev1', name: 'John Berryman' }]);
    (getApplications as jest.Mock).mockResolvedValue(mockApplications);

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText('James Walker')).toBeInTheDocument();
    });
  });

  it('reloads applications when status filter changes', async () => {
    (getActiveRecruiter as jest.Mock).mockReturnValue({ id: 'rev1', name: 'John Berryman' });
    (getRecruiters as jest.Mock).mockResolvedValue([]);
    (getApplications as jest.Mock).mockResolvedValue([]);

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByLabelText('Screening Status')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText('Screening Status'), { target: { value: 'all' } });

    await waitFor(() => {
      expect(getApplications).toHaveBeenCalledWith('all', expect.any(String), expect.anything());
    });
  });
});
