package entities

import "time"

type StudentCSV struct {
	Identification int    `csv:"Documento"`
	Name           string `csv:"Nombre"`
}
type Student struct {
	Identification string    `json:"identification,omitempty" csv:"Documento"`
	Name           string    `json:"name,omitempty" csv:"Nombre"`
	GroupId        string    `json:"group_id,omitempty"`
	Period         string    `json:"period,omitempty"`
	CreatedAt      time.Time `json:"created_at,omitempty"`
}
