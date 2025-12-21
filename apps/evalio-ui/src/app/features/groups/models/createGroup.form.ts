import * as Yup from 'yup';

export interface CreateGroupForm {
  file: File | null;
  groupName: string;
  period: string;
  subjectName: string;
}

export const CreateGroupSchema = Yup.object().shape({
  file: Yup.mixed().required('groups.fileRequired'),
  groupName: Yup.string().required('groups.groupNameRequired'),
  period: Yup.string().required('groups.periodRequired'),
  subjectName: Yup.string().required('groups.subjectNameRequired'),
});
