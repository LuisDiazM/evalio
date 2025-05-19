export interface Qualification {
    group_id:    string;
    number:      number;
    id:          string;
    period:      string;
    template_id: string;
    created_at:  Date;
    updated_at:  Date;
    students:    Student[];
}

export interface Student {
    score:                  number;
    student_name:           string;
    student_identification: number;
    exam_path:              string;
}