import * as Yup from 'yup';

export interface CreateTemplateForm {
  group_id: string;
  number: number;
  period: string;
  subject_name: string;
  questionsCount: number;
  questions: Array<{ question: number; answer: string }>;
}

export const CreateTemplateSchema = Yup.object().shape({
  group_id: Yup.string().required('groups.groupIdRequired'),
  number: Yup.number().min(1).max(5).required('groups.numberRequired'),
  period: Yup.string().required('groups.periodRequired'),
  subject_name: Yup.string().required('groups.subjectNameRequired'),
  questionsCount: Yup.number().min(1).required('groups.questionsCountRequired'),
  questions: Yup.array().of(
    Yup.object({ question: Yup.number().required(), answer: Yup.string().required('groups.answerRequired') })
  ),
});

export default CreateTemplateSchema;
