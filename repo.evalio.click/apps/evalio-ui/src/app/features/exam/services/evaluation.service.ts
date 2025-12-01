import api from '@/shared/services/api';

export interface ExamResponse {
  group_id: string;
  created_at: Date;
  student_identification: number;
  student_name: string;
  exam_path: string;
  template_id: string;
  period: string;
  status: string;
  group_name: string;
}

export async function uploadExam(form: FormData): Promise<ExamResponse | null> {
  const response = await api.post('/manager/exam', form);
  if (response.status !== 201) {
    return null;
  } else {
    const message = `Failed to upload exam: ${response.status}`;
    throw new Error(message);
  }
}
