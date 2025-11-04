export interface ExamResponse {
    group_id:               string;
    created_at:             Date;
    student_identification: number;
    student_name:           string;
    exam_path:              string;
    template_id:            string;
    period:                 string;
    status:                 string;
    group_name:             string;
}