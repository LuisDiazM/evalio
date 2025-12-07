package presenters

import "time"

type ProfessorRequest struct {
	Email    string `json:"email"`
	Name     string `json:"name"`
	Password string `json:"password"`
}

type ProfessorResponse struct {
	ID string `json:"id"`
}

type ProfessorErrorResponse struct {
	Error string `json:"error"`
}

type ProfessorInfo struct {
	ID        string    `json:"id"`
	CreatedAt time.Time `json:"created_at,omitempty"`
	UpdatedAt time.Time `json:"updated_at,omitempty" `
	Email     string    `json:"email,omitempty"`
	Name      string    `json:"name,omitempty"`
}
