interface Props {
  status: string;
}

export default function StatusBadge({ status }: Props) {
  const getStatusStyles = (status: string) => {
    switch (status) {
      case 'waiting_for_recruiter':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'waiting_for_ai':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'waiting_for_candidate':
        return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'advanced':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'declined':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'waiting_for_recruiter':
        return 'Waiting for Recruiter';
      case 'waiting_for_ai':
        return 'Waiting for AI';
      case 'waiting_for_candidate':
        return 'Waiting for Candidate';
      case 'advanced':
        return 'Advanced';
      case 'declined':
        return 'Declined';
      case 'withdrawn':
        return 'Withdrawn';
      default:
        return status;
    }
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getStatusStyles(status)}`}>
      {getStatusLabel(status)}
    </span>
  );
}
