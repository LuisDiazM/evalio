import api from '../api';
import type { ExamResponse } from './entities/exams';
import type { Groups } from './entities/groups';
import type { Qualification } from './entities/qualifications';
import type { CreateTemplate, Template } from './entities/templates';

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

export async function createTemplate(
  templateData: CreateTemplate
): Promise<CreateTemplate | null> {
  const request = await api.post('/template', templateData);
  if (request.status != 200) {
    return null;
  }
  return templateData;
}

export async function deleteGroupById(groupId: string) {
  await api.delete('/group', {
    params: {
      group_id: groupId,
    },
  });
}

export async function deleteTemplateById(templateId: string) {
  await api.delete('/template', {
    params: {
      template_id: templateId,
    },
  });
}

export async function getTemplateSheet(
  groupId: string,
  templateId: string
): Promise<null> {
  const response = await api.get('/template', {
    params: {
      group_id: groupId,
      template_id: templateId,
    },
    responseType: 'blob',
  });

  if (response.status != 200) {
    return null;
  }
  const file = new Blob([response.data], { type: 'application/pdf' });
  const fileURL = URL.createObjectURL(file);
  window.open(fileURL);
  return null;
}

export async function uploadExam(form: FormData): Promise<ExamResponse | null> {
  const response = await api.post('/exam', form);
  if (response.status != 201) {
    return null;
  } else {
    const group = response.data as ExamResponse;
    return group;
  }
}

export async function getExamsByTemplate(
  templateId: string
): Promise<ExamResponse[]> {
  const response = await api.get('/exams', {
    params: {
      template_id: templateId,
    },
  });
  if (response.status != 200) {
    return [];
  }
  const exams = response.data as ExamResponse[];
  return exams;
}

export async function generateCsvSummaryQualifications(templateId: string) {
  const response = await api.get('/summary/export', {
    params: {
      template_id: templateId,
    },
  });
  if (response.status !== 200) {
    return;
  }
  const blob = new Blob([response.data], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'summary.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
