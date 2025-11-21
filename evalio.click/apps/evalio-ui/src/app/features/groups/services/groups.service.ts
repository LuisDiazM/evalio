import api from '@/shared/services/api';

export type Student = { name: string; identification: number };
export type Group = {
  id: string;
  name: string;
  period: string;
  professor_name: string;
  subject_name: string;
  students: Student[];
};

export const fetchGroups = async (): Promise<Group[]> => {
  const url = '/manager/groups';
  const response = await api.get<Group[]>(url, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  throw new Error(`Failed to fetch groups: ${response.status}`);
};

export type CreateGroupPayload = {
  file: File | null;
  name: string;
  subject_name: string;
  period: string;
};

export const createGroup = async (payload: CreateGroupPayload) => {
  const url = '/manager/group';

  const form = new FormData();
  if (payload.file) form.append('file', payload.file, payload.file.name);
  form.append('name', payload.name);
  form.append('subject_name', payload.subject_name);
  form.append('period', payload.period);

  const response = await api.post(url, form, {
    headers: {
      // Let axios set the Content-Type with boundary for multipart/form-data
      'Content-Type': 'multipart/form-data',
    },
    validateStatus: () => true,
  });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  // Try to include server message if provided
  const message = response?.data?.message || `Failed to create group: ${response.status}`;
  throw new Error(message);
};

export const fetchGroupById = async (id: string):Promise<Group> => {
  const url = `/manager/group?id=${id}`;
  const response = await api.get<Group>(url, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  throw new Error(`Failed to fetch group ${id}: ${response.status}`);
};

export type Template = {
  id: string;
  number: number;
  subject_name: string;
  period: string;
  questions: Array<{ question: number; answer: string }>;
  created_at: string;
  group_id: string;
  professor_id: string;
};

export const fetchTemplatesByGroup = async (groupId: string): Promise<Template[]> => {
  const url = `/manager/templates?group_id=${groupId}`;
  const response = await api.get<Template[]>(url, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  throw new Error(`Failed to fetch templates for group ${groupId}: ${response.status}`);
};

export const fetchTemplateById = async (id: string): Promise<Template> => {
  const url = `/manager/template/${id}`;
  const response = await api.get<Template>(url, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  throw new Error(`Failed to fetch template ${id}: ${response.status}`);
};

export type CreateTemplatePayload = {
  group_id: string;
  number: number;
  period: string;
  subject_name: string;
  questions: Array<{ question: number; answer: string }>;
};

export const createTemplate = async (payload: CreateTemplatePayload) => {
  const url = '/manager/template';
  const response = await api.post(url, payload, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  const message = response?.data?.message || `Failed to create template: ${response.status}`;
  throw new Error(message);
};

export type SummaryStudent = {
  score: number;
  student_name: string;
  student_identification: number | string;
  exam_path?: string;
};

export type TemplateSummary = {
  group_id: string;
  number: number;
  id: string;
  period: string;
  template_id: string;
  created_at: string;
  updated_at: string;
  students: SummaryStudent[];
};

export const fetchSummaryByTemplate = async (templateId: string): Promise<TemplateSummary> => {
  const url = `/manager/summary?template_id=${templateId}`;
  const response = await api.get<TemplateSummary>(url, { validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data;
  }

  throw new Error(`Failed to fetch summary for template ${templateId}: ${response.status}`);
};

export const fetchTemplateFile = async (groupId: string, templateId: string): Promise<Blob> => {
  const url = `/manager/template?group_id=${groupId}&template_id=${templateId}`;
  const response = await api.get(url, { responseType: 'blob', validateStatus: () => true });

  if (response.status >= 200 && response.status < 300) {
    return response.data as Blob;
  }

  throw new Error(`Failed to fetch template file: ${response.status}`);
};
