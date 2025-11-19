import api from '@/shared/services/api';

export type Student = { name: string; identification: number };
export type Group = {
  id: string;
  name: string;
  period: string;
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
