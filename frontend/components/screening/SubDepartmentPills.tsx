import { useState } from 'react';
import { SubDepartment } from '@/types/api';

interface Props {
  subDepartments: SubDepartment[];
  onAdd: (subDept: SubDepartment) => void;
  onRemove: (subDept: SubDepartment) => void;
}

const AVAILABLE_SUB_DEPARTMENTS = [
  SubDepartment.ENG_BACKEND,
  SubDepartment.ENG_FRONTEND,
  SubDepartment.ENG_INFRA,
  SubDepartment.ENG_DATA,
  SubDepartment.ENG_SECURITY,
  SubDepartment.PROD_MOBILE,
  SubDepartment.PROD_WEB,
  SubDepartment.PROD_GROWTH,
  SubDepartment.DES_UX,
  SubDepartment.DES_UI,
  SubDepartment.DES_RESEARCH,
  SubDepartment.MKT_CONTENT,
  SubDepartment.MKT_GROWTH,
  SubDepartment.MKT_BRAND,
];

const PILL_COLORS = [
  'bg-blue-100 text-blue-800 border-blue-200',
  'bg-green-100 text-green-800 border-green-200',
  'bg-purple-100 text-purple-800 border-purple-200',
  'bg-pink-100 text-pink-800 border-pink-200',
  'bg-indigo-100 text-indigo-800 border-indigo-200',
  'bg-yellow-100 text-yellow-800 border-yellow-200',
  'bg-red-100 text-red-800 border-red-200',
  'bg-cyan-100 text-cyan-800 border-cyan-200',
];

function getSubDepartmentLabel(subDept: SubDepartment): string {
  return subDept;
}

function getPillColor(index: number): string {
  return PILL_COLORS[index % PILL_COLORS.length];
}

export default function SubDepartmentPills({ subDepartments, onAdd, onRemove }: Props) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchFilter, setSearchFilter] = useState('');

  const availableToAdd = AVAILABLE_SUB_DEPARTMENTS.filter(
    spec => !subDepartments.includes(spec)
  );

  const filteredSubDepartments = searchFilter
    ? availableToAdd.filter(spec => 
        spec.toLowerCase().includes(searchFilter.toLowerCase())
      )
    : availableToAdd;

  const handleAddSubDepartment = (subDept: SubDepartment) => {
    onAdd(subDept);
    setIsModalOpen(false);
    setSearchFilter('');
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Sub-Departments
      </label>
      
      <div className="flex flex-wrap gap-2 mb-3">
        {subDepartments.map((subDept, index) => (
          <div
            key={subDept}
            className={`relative inline-flex items-center px-3 py-1 rounded-full text-sm border ${getPillColor(index)}`}
          >
            <span>{getSubDepartmentLabel(subDept)}</span>
            <button
              type="button"
              onClick={() => onRemove(subDept)}
              className="ml-2 -mr-1 w-4 h-4 rounded-full hover:bg-black/10 flex items-center justify-center"
              aria-label={`Remove ${getSubDepartmentLabel(subDept)}`}
            >
              <svg className="w-3 h-3" viewBox="0 0 12 12" fill="currentColor">
                <path d="M4.5 4.5L7.5 7.5M7.5 4.5L4.5 7.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        ))}
        
        <button
          type="button"
          onClick={() => setIsModalOpen(true)}
          className="inline-flex items-center px-3 py-1 rounded-full text-sm border-2 border-dashed border-gray-300 text-gray-500 hover:border-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add New
        </button>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-30 flex items-center justify-center z-50" onClick={() => setIsModalOpen(false)}>
          <div 
            className="bg-white rounded-lg shadow-lg w-96 max-h-96 flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Add Sub-Department</h3>
            </div>

            <div className="px-6 py-3 border-b border-gray-200">
              <input
                type="text"
                value={searchFilter}
                onChange={(e) => setSearchFilter(e.target.value)}
                placeholder="Search sub-departments..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                autoFocus
              />
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-3">
              {filteredSubDepartments.length > 0 ? (
                <div className="space-y-2">
                  {filteredSubDepartments.map((spec) => (
                    <button
                      key={spec}
                      type="button"
                      onClick={() => handleAddSubDepartment(spec)}
                      className="w-full text-left px-3 py-2 rounded-md hover:bg-gray-100 transition-colors"
                    >
                      <div className="font-medium text-gray-900">{spec}</div>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  {searchFilter ? 'No matching sub-departments found.' : 'All sub-departments already added.'}
                </div>
              )}
            </div>

            <div className="px-6 py-4 border-t border-gray-200 flex justify-end">
              <button
                type="button"
                onClick={() => {
                  setIsModalOpen(false);
                  setSearchFilter('');
                }}
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
