import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import QueuePage from '@/app/queue/page';
import { getApplications } from '@/lib/api';

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

jest.mock('@/lib/api', () => ({
  getApplications: jest.fn(),
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
    region: 'North America/United States',
    screeningStatus: 'waiting_for_recruiter',
    assignee_id: 'rev1',
    assignee_name: 'John Berryman',
    createdAt: '2026-01-01T00:00:00Z',
    updatedAt: '2026-01-02T00:00:00Z',
  },
];

describe('QueuePage', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockSearchParamsGet.mockReturnValue(null);
    (getApplications as jest.Mock).mockResolvedValue([]);
  });

  it('loads applications from current filter/search params', async () => {
    mockSearchParamsGet.mockImplementation((key: string) => {
      if (key === 'filter') return 'all';
      if (key === 'search') return 'frontend';
      return null;
    });

    render(<QueuePage />);

    await waitFor(() => {
      expect(getApplications).toHaveBeenCalledWith('all', 'frontend');
    });

    expect(mockReplace).not.toHaveBeenCalledWith('/login');
  });

  it('shows error state and retry button when API call fails', async () => {
    (getApplications as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText(/Network error/)).toBeInTheDocument();
    });

    expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
  });

  it('shows empty state message when no candidates match filters', async () => {
    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText('No candidates found for this filter.')).toBeInTheDocument();
    });
  });

  it('renders candidate rows when data is returned', async () => {
    (getApplications as jest.Mock).mockResolvedValue(mockApplications);

    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByText('James Walker')).toBeInTheDocument();
    });
  });

  it('reloads applications when status filter changes', async () => {
    render(<QueuePage />);

    await waitFor(() => {
      expect(screen.getByLabelText('Screening Status')).toBeInTheDocument();
    });

    fireEvent.change(screen.getByLabelText('Screening Status'), { target: { value: 'all' } });

    await waitFor(() => {
      expect(getApplications).toHaveBeenCalledWith('all', expect.any(String));
    });
  });
});
