import { useRouter } from 'next/navigation';
import { ApplicationSummary } from '@/types/api';
import StatusBadge from './StatusBadge';

interface Props {
  applications: ApplicationSummary[];
}

export default function CandidateTable({ applications }: Props) {
  const router = useRouter();

  const handleRowClick = (applicationId: string) => {
    router.push(`/review/${applicationId}`);
  };

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Email
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Company
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Job Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">
              Department
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Region
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">
              Applied
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">
              Updated
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
              Assignee
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {applications.map((application) => (
            <CandidateTableRow 
              key={application.id} 
              application={application} 
              onRowClick={handleRowClick}
            />
          ))}
        </tbody>
        </table>
      </div>
    </div>
  );
}

interface RowProps {
  application: ApplicationSummary;
  onRowClick: (applicationId: string) => void;
}

function CandidateTableRow({ application, onRowClick }: RowProps) {
  const createdDate = new Date(application.createdAt).toLocaleDateString();
  const updatedDate = new Date(application.updatedAt).toLocaleDateString();

  return (
    <tr 
      className="hover:bg-gray-50 cursor-pointer transition-colors"
      onClick={() => onRowClick(application.id)}
    >
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm font-medium text-gray-900">
          {application.firstName} {application.lastName}
        </div>
      </td>
      <td className="px-4 py-4">
        <div className="text-sm text-gray-900 truncate max-w-xs" title={application.email}>
          {application.email}
        </div>
      </td>
      <td className="px-4 py-4">
        <div className="text-sm text-gray-900 truncate max-w-xs" title={application.companyName}>
          {application.companyName}
        </div>
      </td>
      <td className="px-4 py-4">
        <div className="text-sm text-gray-900 truncate max-w-xs" title={application.jobTitle}>
          {application.jobTitle}
        </div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">
          {application.department}
        </div>
      </td>
      <td className="px-4 py-4">
        <div className="text-sm text-gray-900 truncate max-w-xs">{application.region}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <StatusBadge status={application.screeningStatus} />
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-500">{createdDate}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-500">{updatedDate}</div>
      </td>
      <td className="px-4 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">
          {application.assignee_name || <span className="text-gray-400 italic">Unassigned</span>}
        </div>
      </td>
    </tr>
  );
}
