package entities

import "time"

type Student struct {
	Identification string    `json:"identification,omitempty"`
	Name           string    `json:"name,omitempty"`
	GroupId        string    `json:"group_id,omitempty"`
	Period         string    `json:"period,omitempty"`
	CreatedAt      time.Time `json:"created_at,omitempty"`
}
