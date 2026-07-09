import { Application, Department, SubDepartment } from '@/types/api';
import SubDepartmentPills from './SubDepartmentPills';

interface Props {
  application: Application;
  hasChanges: boolean;
  onFirstNameChange: (value: string) => void;
  onLastNameChange: (value: string) => void;
  onFieldChange: (
    field: 'email' | 'mobile' | 'bio' | 'linkedinUrl',
    value: string
  ) => void;
  onJobOpeningFieldChange: (
    field: 'title' | 'department' | 'seniorityLevel' | 'jobDescription',
    value: string
  ) => void;
  onCompanyFieldChange: (field: 'name' | 'size' | 'siteUrl', value: string) => void;
  onSubDepartmentAdd: (subDept: SubDepartment) => void;
  onSubDepartmentRemove: (subDept: SubDepartment) => void;
  onSave: () => Promise<void>;
}

export default function CandidateDetailsPane({
  application,
  hasChanges,
  onFirstNameChange,
  onLastNameChange,
  onFieldChange,
  onJobOpeningFieldChange,
  onCompanyFieldChange,
  onSubDepartmentAdd,
  onSubDepartmentRemove,
  onSave,
}: Props) {
  return (
    <div className="flex-1 bg-white rounded-lg shadow overflow-y-auto">
      <div className="p-6 space-y-8">
        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Candidate Details</h2>
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                <input
                  type="text"
                  value={application.firstName}
                  onChange={(e) => onFirstNameChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                <input
                  type="text"
                  value={application.lastName}
                  onChange={(e) => onLastNameChange(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={application.email}
                  onChange={(e) => onFieldChange('email', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="text"
                  value={application.mobile}
                  onChange={(e) => onFieldChange('mobile', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
              <textarea
                value={application.bio}
                onChange={(e) => onFieldChange('bio', e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn URL</label>
              <input
                type="url"
                value={application.linkedinUrl}
                onChange={(e) => onFieldChange('linkedinUrl', e.target.value)}
                placeholder="https://linkedin.com/in/username"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </section>

        <section className="border-t border-gray-200 pt-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-2">Job Opening</h2>
          <p className="text-sm text-gray-500 mb-6">
            The role this candidate is being screened for, including the hiring company.
          </p>

          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                <input
                  type="text"
                  value={application.jobOpening.title}
                  onChange={(e) => onJobOpeningFieldChange('title', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Seniority Level</label>
                <select
                  value={application.jobOpening.seniorityLevel}
                  onChange={(e) => onJobOpeningFieldChange('seniorityLevel', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="Senior">Senior</option>
                  <option value="Mid">Mid</option>
                  <option value="Junior">Junior</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Department</label>
                <select
                  value={application.jobOpening.department}
                  onChange={(e) => onJobOpeningFieldChange('department', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value={Department.ENGINEERING}>Engineering</option>
                  <option value={Department.PRODUCT}>Product</option>
                  <option value={Department.DESIGN}>Design</option>
                  <option value={Department.MARKETING}>Marketing</option>
                  <option value={Department.SALES}>Sales</option>
                  <option value={Department.FINANCE}>Finance</option>
                  <option value={Department.OPERATIONS}>Operations</option>
                  <option value={Department.LEGAL}>Legal</option>
                </select>
              </div>
              <div>
                <SubDepartmentPills
                  subDepartments={application.jobOpening.subDepartments}
                  onAdd={onSubDepartmentAdd}
                  onRemove={onSubDepartmentRemove}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Job Description</label>
              <textarea
                value={application.jobOpening.jobDescription}
                onChange={(e) => onJobOpeningFieldChange('jobDescription', e.target.value)}
                rows={8}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Hiring Company</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
                  <input
                    type="text"
                    value={application.jobOpening.company.name}
                    onChange={(e) => onCompanyFieldChange('name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company Size</label>
                  <input
                    type="text"
                    value={application.jobOpening.company.size}
                    onChange={(e) => onCompanyFieldChange('size', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Website</label>
                  <input
                    type="url"
                    value={application.jobOpening.company.siteUrl}
                    onChange={(e) => onCompanyFieldChange('siteUrl', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <div className="pt-2">
          <button
            type="button"
            onClick={() => {
              void onSave();
            }}
            className={`px-6 py-2 rounded-md transition-colors ${
              hasChanges
                ? 'bg-blue-600 text-white hover:bg-blue-700'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
            disabled={!hasChanges}
          >
            Update Details
          </button>
        </div>
      </div>
    </div>
  );
}
