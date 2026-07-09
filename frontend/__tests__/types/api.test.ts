/**
 * Tests for API schema types
 */

import {
  Application,
  ApplicationSummary,
  Department,
  JobOpening,
  NewUpdateRequest,
  Recruiter,
  SubDepartment,
  Update,
} from '@/types/api';

describe('API Schema Types', () => {
  describe('Enums', () => {
    it('should have Department enum with expected values', () => {
      expect(Department.ENGINEERING).toBe('ENGINEERING');
      expect(Department.PRODUCT).toBe('PRODUCT');
      expect(Department.DESIGN).toBe('DESIGN');
      expect(Department.MARKETING).toBe('MARKETING');
      expect(Department.SALES).toBe('SALES');
      expect(Department.FINANCE).toBe('FINANCE');
      expect(Department.OPERATIONS).toBe('OPERATIONS');
      expect(Department.LEGAL).toBe('LEGAL');
    });

    it('should have SubDepartment enum with expected values', () => {
      expect(SubDepartment.ENG_BACKEND).toBe('ENG_BACKEND');
      expect(SubDepartment.ENG_FRONTEND).toBe('ENG_FRONTEND');
      expect(SubDepartment.ENG_INFRA).toBe('ENG_INFRA');
      expect(SubDepartment.ENG_DATA).toBe('ENG_DATA');
      expect(SubDepartment.ENG_SECURITY).toBe('ENG_SECURITY');
      expect(SubDepartment.PROD_MOBILE).toBe('PROD_MOBILE');
      expect(SubDepartment.PROD_WEB).toBe('PROD_WEB');
      expect(SubDepartment.PROD_GROWTH).toBe('PROD_GROWTH');
      expect(SubDepartment.DES_UX).toBe('DES_UX');
      expect(SubDepartment.DES_UI).toBe('DES_UI');
      expect(SubDepartment.DES_RESEARCH).toBe('DES_RESEARCH');
      expect(SubDepartment.MKT_CONTENT).toBe('MKT_CONTENT');
      expect(SubDepartment.MKT_GROWTH).toBe('MKT_GROWTH');
      expect(SubDepartment.MKT_BRAND).toBe('MKT_BRAND');
    });
  });

  describe('Type Compatibility', () => {
    it('should accept JobOpening with hiring company details', () => {
      const jobOpening: JobOpening = {
        title: 'Senior Engineer',
        seniorityLevel: 'Senior',
        department: Department.ENGINEERING,
        subDepartments: [SubDepartment.ENG_BACKEND],
        jobDescription: 'Build agent systems and backend services.',
        company: {
          id: 'comp-id',
          name: 'TestCo',
          siteUrl: 'https://example.com',
          size: '10-49',
          address: {
            address1: '123 Main St',
            country: 'US',
            id: 'addr-id',
            locality: 'City',
            postalCode: '12345',
            region: 'State'
          }
        }
      };

      expect(jobOpening.company.name).toBe('TestCo');
      expect(jobOpening.subDepartments).toEqual(['ENG_BACKEND']);
    });

    it('should accept Application with nested jobOpening', () => {
      const application: Application = {
        id: 'test-id',
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        mobile: '+1234567890',
        bio: 'Test bio',
        linkedinUrl: 'https://linkedin.com/in/johndoe',
        jobOpening: {
          title: 'Senior Engineer',
          seniorityLevel: 'Senior',
          department: Department.ENGINEERING,
          subDepartments: [SubDepartment.ENG_BACKEND],
          jobDescription: 'Build agent systems and backend services.',
          company: {
            id: 'comp-id',
            name: 'TestCo',
            siteUrl: 'https://example.com',
            size: '10-49',
            address: {
              address1: '123 Main St',
              country: 'US',
              id: 'addr-id',
              locality: 'City',
              postalCode: '12345',
              region: 'State'
            }
          }
        },
        assignee_id: 'rec1',
        region: 'North America/United States',
        screeningStatus: 'waiting_for_recruiter',
        createdAt: '2026-03-27T10:00:00Z',
        updatedAt: '2026-03-27T10:00:00Z',
        locale: {
          country: 'US',
          preferredLanguage: 'en-US',
          region: 'NA',
          storeId: 'us'
        },
        updates: []
      };

      expect(application.assignee_id).toBe('rec1');
      expect(application.region).toBe('North America/United States');
      expect(application.jobOpening.department).toBe('ENGINEERING');
      expect(application.jobOpening.subDepartments).toEqual(['ENG_BACKEND']);
    });

    it('should accept ApplicationSummary with job opening summary fields', () => {
      const summary: ApplicationSummary = {
        id: 'test-id',
        firstName: 'John',
        lastName: 'Doe',
        email: 'john@example.com',
        mobile: '+1234567890',
        jobTitle: 'Engineer',
        seniorityLevel: 'Senior',
        department: Department.ENGINEERING,
        companyName: 'TestCo',
        region: 'North America/United States',
        assignee_id: 'rec1',
        assignee_name: 'Jane Recruiter',
        screeningStatus: 'waiting_for_recruiter',
        createdAt: '2026-03-27T10:00:00Z',
        updatedAt: '2026-03-27T10:00:00Z'
      };

      expect(summary.assignee_id).toBe('rec1');
      expect(summary.assignee_name).toBe('Jane Recruiter');
      expect(summary.department).toBe('ENGINEERING');
    });

    it('should accept Update with internal_notes field', () => {
      const update: Update = {
        id: 'update-id',
        timestamp: '2026-03-27T10:00:00Z',
        actor: 'human_recruiter',
        internal_notes: 'Test internal notes',
        update_type: 'advance',
        correspondence: 'Welcome!'
      };

      expect(update.internal_notes).toBe('Test internal notes');
    });

    it('should accept NewUpdateRequest with internal_notes field', () => {
      const request: NewUpdateRequest = {
        update_type: 'general_update',
        internal_notes: 'Test notes',
        correspondence: 'Test message'
      };

      expect(request.internal_notes).toBe('Test notes');
    });

    it('should accept Recruiter type', () => {
      const recruiter: Recruiter = {
        id: 'rec1',
        name: 'Jane Recruiter'
      };

      expect(recruiter.id).toBe('rec1');
      expect(recruiter.name).toBe('Jane Recruiter');
    });
  });

  describe('Optional Fields', () => {
    it('should allow Application with null assignee_id and region', () => {
      const application: Application = {
        id: 'test-id',
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@example.com',
        mobile: '+1234567890',
        bio: 'Test bio',
        linkedinUrl: 'https://linkedin.com/in/janedoe',
        jobOpening: {
          title: 'Principal Designer',
          seniorityLevel: 'Senior',
          department: Department.DESIGN,
          subDepartments: [SubDepartment.DES_UX, SubDepartment.DES_UI],
          jobDescription: 'Lead a design systems and product design practice.',
          company: {
            id: 'comp-id',
            name: 'TestCo',
            siteUrl: 'https://example.com',
            size: '10-49',
            address: {
              address1: '456 Oak St',
              country: 'US',
              id: 'addr-id',
              locality: 'City',
              postalCode: '12345',
              region: 'State'
            }
          }
        },
        assignee_id: undefined,
        region: undefined,
        screeningStatus: 'waiting_for_candidate',
        createdAt: '2026-03-27T10:00:00Z',
        updatedAt: '2026-03-27T10:00:00Z',
        locale: {
          country: 'US',
          preferredLanguage: 'en-US',
          region: 'NA',
          storeId: 'us'
        },
        updates: []
      };

      expect(application.assignee_id).toBeUndefined();
      expect(application.region).toBeUndefined();
      expect(application.jobOpening.subDepartments).toHaveLength(2);
    });

    it('should allow ApplicationSummary with null assignee fields', () => {
      const summary: ApplicationSummary = {
        id: 'test-id',
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane@example.com',
        mobile: '+1234567890',
        jobTitle: 'Designer',
        seniorityLevel: 'Senior',
        department: Department.DESIGN,
        companyName: 'TestCo',
        region: 'North America/Canada',
        assignee_id: undefined,
        assignee_name: undefined,
        screeningStatus: 'waiting_for_candidate',
        createdAt: '2026-03-27T10:00:00Z',
        updatedAt: '2026-03-27T10:00:00Z'
      };

      expect(summary.assignee_id).toBeUndefined();
      expect(summary.assignee_name).toBeUndefined();
    });
  });
});
