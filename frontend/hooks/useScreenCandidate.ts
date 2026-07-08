import { useCallback, useEffect, useState } from 'react';
import { addUpdate, getApplication, updateApplication } from '@/lib/api';
import { DEFAULT_REVIEWER_ID } from '@/lib/defaultReviewer';
import { Application, ApplicationUpdateRequest, NewUpdateRequest, SubDepartment } from '@/types/api';

type EditableApplicationField =
  | 'email'
  | 'mobile'
  | 'bio'
  | 'linkedinUrl'
  | 'jobTitle'
  | 'department'
  | 'seniorityLevel';

type EditableCompanyField = 'name' | 'size' | 'type' | 'verificationStatus' | 'siteUrl';

function toUpdateRequest(
  original: Application,
  edited: Application
): ApplicationUpdateRequest {
  const request: ApplicationUpdateRequest = {};

  if (edited.firstName !== original.firstName) request.firstName = edited.firstName;
  if (edited.lastName !== original.lastName) request.lastName = edited.lastName;
  if (edited.email !== original.email) request.email = edited.email;
  if (edited.mobile !== original.mobile) request.mobile = edited.mobile;
  if (edited.bio !== original.bio) request.bio = edited.bio;
  if (edited.linkedinUrl !== original.linkedinUrl) request.linkedinUrl = edited.linkedinUrl;
  if (edited.jobTitle !== original.jobTitle) request.jobTitle = edited.jobTitle;
  if (edited.seniorityLevel !== original.seniorityLevel) request.seniorityLevel = edited.seniorityLevel;
  if (edited.department !== original.department) {
    request.department = edited.department;
  }
  if (JSON.stringify(edited.subDepartments) !== JSON.stringify(original.subDepartments)) {
    request.subDepartments = edited.subDepartments;
  }

  if (edited.company.name !== original.company.name) {
    request.companyName = edited.company.name;
  }
  if (edited.company.size !== original.company.size) {
    request.companySize = edited.company.size;
  }
  if (edited.company.type !== original.company.type) {
    request.companyType = edited.company.type;
  }
  if (edited.company.verificationStatus !== original.company.verificationStatus) {
    request.companyVerificationStatus = edited.company.verificationStatus;
  }
  if (edited.company.siteUrl !== original.company.siteUrl) {
    request.companySiteUrl = edited.company.siteUrl;
  }

  return request;
}

export function useScreenCandidate(applicationId: string | null) {
  const [application, setApplication] = useState<Application | null>(null);
  const [editedApplication, setEditedApplication] = useState<Application | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submittingUpdate, setSubmittingUpdate] = useState(false);
  const [hasChanges, setHasChanges] = useState(false);

  const markDirty = useCallback(
    (next: Application) => {
      setEditedApplication(next);
      setHasChanges(JSON.stringify(next) !== JSON.stringify(application));
    },
    [application]
  );

  const loadApplication = useCallback(async () => {
    if (!applicationId) return;

    try {
      setLoading(true);
      setError(null);
      const data = await getApplication(applicationId);
      setApplication(data);
      setEditedApplication(data);
      setHasChanges(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load application');
    } finally {
      setLoading(false);
    }
  }, [applicationId]);

  useEffect(() => {
    loadApplication();
  }, [loadApplication]);

  const updateFirstName = useCallback(
    (firstName: string) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        firstName: firstName,
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const updateLastName = useCallback(
    (lastName: string) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        lastName: lastName,
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const updateField = useCallback(
    (field: EditableApplicationField, value: string) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        [field]: value,
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const updateCompanyField = useCallback(
    (field: EditableCompanyField, value: string) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        company: {
          ...editedApplication.company,
          [field]: value,
        },
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const addSubDepartment = useCallback(
    (subDept: SubDepartment) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        subDepartments: [...editedApplication.subDepartments, subDept],
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const removeSubDepartment = useCallback(
    (subDept: SubDepartment) => {
      if (!editedApplication) return;
      const next: Application = {
        ...editedApplication,
        subDepartments: editedApplication.subDepartments.filter(
          (s) => s !== subDept
        ),
      };
      markDirty(next);
    },
    [editedApplication, markDirty]
  );

  const saveApplication = useCallback(async () => {
    if (!applicationId || !application || !editedApplication || !hasChanges) return;
    const request = toUpdateRequest(application, editedApplication);
    await updateApplication(applicationId, request);
    await loadApplication();
  }, [applicationId, application, editedApplication, hasChanges, loadApplication]);

  const submitUpdate = useCallback(
    async (updateData: NewUpdateRequest) => {
      if (!applicationId) return;
      try {
        setSubmittingUpdate(true);
        await addUpdate(applicationId, {
          ...updateData,
          recruiter_id: DEFAULT_REVIEWER_ID,
        });
        await loadApplication();
      } finally {
        setSubmittingUpdate(false);
      }
    },
    [applicationId, loadApplication]
  );

  return {
    application,
    editedApplication,
    loading,
    error,
    submittingUpdate,
    hasChanges,
    loadApplication,
    updateFirstName,
    updateLastName,
    updateField,
    updateCompanyField,
    addSubDepartment,
    removeSubDepartment,
    saveApplication,
    submitUpdate,
  };
}
