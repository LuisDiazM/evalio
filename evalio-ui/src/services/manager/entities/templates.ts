export interface Template {
  id: string;
  professor_id: string;
  created_at: Date;
  questions: Question[];
  subject_name: string;
  period: string;
  number: number;
  group_id: string;
}

export interface Question {
  question: number;
  answer: string;
}

export interface CreateTemplate {
  subject_name: string;
  period: string;
  number: number;
  group_id: string;
  questions: Question[];
}
