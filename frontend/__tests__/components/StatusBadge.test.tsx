import { render, screen } from '@testing-library/react';
import StatusBadge from '@/components/StatusBadge';

describe('StatusBadge', () => {
  it('should render waiting_for_recruiter status correctly', () => {
    render(<StatusBadge status="waiting_for_recruiter" />);
    expect(screen.getByText('Waiting for Recruiter')).toBeInTheDocument();
  });

  it('should render advanced status correctly', () => {
    render(<StatusBadge status="advanced" />);
    expect(screen.getByText('Advanced')).toBeInTheDocument();
  });

  it('should render declined status correctly', () => {
    render(<StatusBadge status="declined" />);
    expect(screen.getByText('Declined')).toBeInTheDocument();
  });

  it('should render waiting_for_ai status correctly', () => {
    render(<StatusBadge status="waiting_for_ai" />);
    expect(screen.getByText('Waiting for AI')).toBeInTheDocument();
  });

  it('should render waiting_for_candidate status correctly', () => {
    render(<StatusBadge status="waiting_for_candidate" />);
    expect(screen.getByText('Waiting for Candidate')).toBeInTheDocument();
  });

  it('should render withdrawn status correctly', () => {
    render(<StatusBadge status="withdrawn" />);
    expect(screen.getByText('Withdrawn')).toBeInTheDocument();
  });

  it('should render unknown status as-is', () => {
    render(<StatusBadge status="unknown_status" />);
    expect(screen.getByText('unknown_status')).toBeInTheDocument();
  });

  it('should apply correct CSS classes for different statuses', () => {
    const { rerender } = render(<StatusBadge status="advanced" />);
    expect(screen.getByText('Advanced')).toHaveClass('text-green-800');

    rerender(<StatusBadge status="declined" />);
    expect(screen.getByText('Declined')).toHaveClass('text-red-800');

    rerender(<StatusBadge status="waiting_for_recruiter" />);
    expect(screen.getByText('Waiting for Recruiter')).toHaveClass('text-yellow-800');
  });
});
