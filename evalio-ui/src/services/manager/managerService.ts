import api from '../api';
import type { Groups } from './entities/groups';
import type { Qualification } from './entities/qualifications';
import type { Template } from './entities/templates';

export async function getGroupsByProfessor(): Promise<Groups[]> {
  const request = await api.get('/groups');
  if (request.status === 204 || request.status !== 200) {
    return [];
  }
  const groupsData = request.data as Groups[];

  return groupsData;
}

export async function getGroupById(groupId: string): Promise<Groups | null> {
  const request = await api.get('/group', {
    params: {
      id: groupId,
    },
  });
  if (request.status === 204 || request.status !== 200) {
    return null;
  }
  const group = request.data as Groups;
  return group;
}

export async function getTemplatesByGroup(
  groupId: string
): Promise<Template[]> {
  const request = await api.get('/templates', {
    params: {
      group_id: groupId,
    },
  });
  if (request.status === 204 || request.status !== 200) {
    return [];
  }
  const template = request.data as Template[];
  return template;
}

export async function getTemplateById(id: string): Promise<Template | null> {
  const request = await api.get(`/template/${id}`);
  if (request.status === 204 || request.status !== 200) {
    return null;
  }
  const template = request.data as Template;
  return template;
}

export async function createGroup(form: FormData): Promise<Groups | null> {
  const response = await api.post('/group', form);
  if (response.status != 200) {
    return null;
  }
  const group = response.data as Groups;
  return group;
}

export async function getSummaryByTemplateId(
  templateId: string
): Promise<Qualification | null> {
  const request = await api.get('/summary', {
    params: {
      template_id: templateId,
    },
  });
  if (request.status === 204 || request.status !== 200) {
    return null;
  }
  const template = request.data as Qualification;
  return template;
}
