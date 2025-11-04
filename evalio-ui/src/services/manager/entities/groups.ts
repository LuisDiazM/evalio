export interface Groups {
    id:             string;
    name:           string;
    period:         string;
    subject_name:   string;
    created_at:     Date;
    professor_id:   string;
    professor_name: string;
    students:       Student[];
}

export interface Student {
    name:           string;
    identification: number;
}