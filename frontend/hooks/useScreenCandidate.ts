import { useCallback, useEffect, useState } from 'react';
import { addUpdate, getApplication, updateApplication } from '@/lib/api';
import { DEFAULT_REVIEWER_ID } from '@/lib/defaultReviewer';
import { Application, ApplicationUpdateRequest, NewUpdateRequest, SubDepartment } from '@/types/api';

type EditableApplicationField = 'email' | 'mobile' | 'bio' | 'linkedinUrl';
type EditableJobOpeningField = 'title' | 'department' | 'seniorityLevel' | 'jobDescription';
type EditableCompanyField = 'name' | 'size' | 'siteUrl';

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

  if (edited.jobOpening.title !== original.jobOpening.title) {
    request.jobTitle = edited.jobOpening.title;
  }
  if (edited.jobOpening.seniorityLevel !== original.jobOpening.seniorityLevel) {
    request.seniorityLevel = edited.jobOpening.seniorityLevel;
  }
  if (edited.jobOpening.department !== original.jobOpening.department) {
    request.department = edited.jobOpening.department;
  }
  if (
    JSON.stringify(edited.jobOpening.subDepartments) !==
    JSON.stringify(original.jobOpening.subDepartments)
  ) {
    request.subDepartments = edited.jobOpening.subDepartments;
  }
  if (edited.jobOpening.jobDescription !== original.jobOpening.jobDescription) {
    request.jobDescription = edited.jobOpening.jobDescription;
  }

  if (edited.jobOpening.company.name !== original.jobOpening.company.name) {
    request.companyName = edited.jobOpening.company.name;
  }
  if (edited.jobOpening.company.size !== original.jobOpening.company.size) {
    request.companySize = edited.jobOpening.company.size;
  }
  if (edited.jobOpening.company.siteUrl !== original.jobOpening.company.siteUrl) {
    request.companySiteUrl = edited.jobOpening.company.siteUrl;
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
      markDirty({ ...editedApplication, firstName });
    },
    [editedApplication, markDirty]
  );

  const updateLastName = useCallback(
    (lastName: string) => {
      if (!editedApplication) return;
      markDirty({ ...editedApplication, lastName });
    },
    [editedApplication, markDirty]
  );

  const updateField = useCallback(
    (field: EditableApplicationField, value: string) => {
      if (!editedApplication) return;
      markDirty({
        ...editedApplication,
        [field]: value,
      });
    },
    [editedApplication, markDirty]
  );

  const updateJobOpeningField = useCallback(
    (field: EditableJobOpeningField, value: string) => {
      if (!editedApplication) return;
      markDirty({
        ...editedApplication,
        jobOpening: {
          ...editedApplication.jobOpening,
          [field]: value,
        },
      });
    },
    [editedApplication, markDirty]
  );

  const updateCompanyField = useCallback(
    (field: EditableCompanyField, value: string) => {
      if (!editedApplication) return;
      markDirty({
        ...editedApplication,
        jobOpening: {
          ...editedApplication.jobOpening,
          company: {
            ...editedApplication.jobOpening.company,
            [field]: value,
          },
        },
      });
    },
    [editedApplication, markDirty]
  );

  const addSubDepartment = useCallback(
    (subDept: SubDepartment) => {
      if (!editedApplication) return;
      markDirty({
        ...editedApplication,
        jobOpening: {
          ...editedApplication.jobOpening,
          subDepartments: [...editedApplication.jobOpening.subDepartments, subDept],
        },
      });
    },
    [editedApplication, markDirty]
  );

  const removeSubDepartment = useCallback(
    (subDept: SubDepartment) => {
      if (!editedApplication) return;
      markDirty({
        ...editedApplication,
        jobOpening: {
          ...editedApplication.jobOpening,
          subDepartments: editedApplication.jobOpening.subDepartments.filter(
            (s) => s !== subDept
          ),
        },
      });
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
    updateJobOpeningField,
    updateCompanyField,
    addSubDepartment,
    removeSubDepartment,
    saveApplication,
    submitUpdate,
  };
}
