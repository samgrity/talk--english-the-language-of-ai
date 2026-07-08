import { render, screen, fireEvent } from '@testing-library/react';
import CandidateTable from '@/components/CandidateTable';
import { ApplicationSummary } from '@/types/api';

const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
}));

const mockApplications: ApplicationSummary[] = [
  {
    id: 'test-id-1',
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@example.com',
    mobile: '+1-555-123-4567',
    jobTitle: 'Senior Engineer',
    seniorityLevel: 'Senior',
    department: 'ENGINEERING',
    companyName: 'Test Company',
    companySize: 'Large',
    companyType: 'Enterprise',
    region: 'North America',
    screeningStatus: 'waiting_for_recruiter',
    createdAt: '2026-03-27T10:00:00Z',
    updatedAt: '2026-03-27T11:00:00Z',
  },
  {
    id: 'test-id-2',
    firstName: 'Jane',
    lastName: 'Smith',
    email: 'jane.smith@example.com',
    mobile: '+1-555-987-6543',
    jobTitle: 'Product Manager',
    seniorityLevel: 'Mid',
    department: 'DESIGN',
    companyName: 'Another Company',
    companySize: 'Medium',
    companyType: 'Agency',
    region: 'Europe',
    screeningStatus: 'advanced',
    createdAt: '2026-03-26T09:00:00Z',
    updatedAt: '2026-03-27T09:00:00Z',
  },
];

describe('CandidateTable', () => {
  beforeEach(() => {
    mockPush.mockClear();
  });

  it('should render table headers correctly', () => {
    render(<CandidateTable applications={mockApplications} />);

    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Email')).toBeInTheDocument();
    expect(screen.getByText('Company')).toBeInTheDocument();
    expect(screen.getByText('Job Title')).toBeInTheDocument();
    expect(screen.getByText('Department')).toBeInTheDocument();
    expect(screen.getByText('Region')).toBeInTheDocument();
    expect(screen.getByText('Status')).toBeInTheDocument();
    expect(screen.getByText('Applied')).toBeInTheDocument();
    expect(screen.getByText('Updated')).toBeInTheDocument();
    expect(screen.getByText('Assignee')).toBeInTheDocument();
  });

  it('should render application data in table rows', () => {
    render(<CandidateTable applications={mockApplications} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john.doe@example.com')).toBeInTheDocument();
    expect(screen.getByText('Test Company')).toBeInTheDocument();
    expect(screen.getByText('Waiting for Recruiter')).toBeInTheDocument();

    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('jane.smith@example.com')).toBeInTheDocument();
    expect(screen.getByText('Another Company')).toBeInTheDocument();
    expect(screen.getByText('Advanced')).toBeInTheDocument();
  });

  it('should navigate to review page when row is clicked', () => {
    render(<CandidateTable applications={mockApplications} />);

    const firstRow = screen.getByText('John Doe').closest('tr');
    expect(firstRow).toBeInTheDocument();
    
    fireEvent.click(firstRow!);
    expect(mockPush).toHaveBeenCalledWith('/review/test-id-1');

    const secondRow = screen.getByText('Jane Smith').closest('tr');
    expect(secondRow).toBeInTheDocument();
    
    fireEvent.click(secondRow!);
    expect(mockPush).toHaveBeenCalledWith('/review/test-id-2');
  });

  it('should display formatted dates', () => {
    render(<CandidateTable applications={mockApplications} />);

    expect(screen.getByRole('table')).toHaveTextContent(/\d+\/\d+\/\d+/);
  });

  it('should render empty table when no applications provided', () => {
    render(<CandidateTable applications={[]} />);

    expect(screen.getByText('Name')).toBeInTheDocument();
    const tableBody = screen.getByRole('table').querySelector('tbody');
    expect(tableBody?.children).toHaveLength(0);
  });

  it('should have proper table structure and styling', () => {
    render(<CandidateTable applications={mockApplications} />);

    const table = screen.getByRole('table');
    expect(table).toHaveClass('w-full');
    expect(screen.getByRole('table')).toContainElement(screen.getByRole('columnheader', { name: 'Name' }));
  });

  it('should render different status badges correctly', () => {
    const mixedStatusApps: ApplicationSummary[] = [
      { ...mockApplications[0], screeningStatus: 'waiting_for_recruiter', id: 't1' },
      { ...mockApplications[0], screeningStatus: 'advanced', id: 't2' },
      { ...mockApplications[0], screeningStatus: 'declined', id: 't3' },
      { ...mockApplications[0], screeningStatus: 'waiting_for_candidate', id: 't4' },
    ];

    render(<CandidateTable applications={mixedStatusApps} />);

    expect(screen.getByText('Waiting for Recruiter')).toBeInTheDocument();
    expect(screen.getByText('Advanced')).toBeInTheDocument();
    expect(screen.getByText('Declined')).toBeInTheDocument();
    expect(screen.getByText('Waiting for Candidate')).toBeInTheDocument();
  });

  it('should have hover effects and cursor pointer on clickable table rows', () => {
    render(<CandidateTable applications={mockApplications} />);

    const firstRow = screen.getByText('John Doe').closest('tr');
    expect(firstRow).toHaveClass('hover:bg-gray-50');
    expect(firstRow).toHaveClass('cursor-pointer');
  });
});
