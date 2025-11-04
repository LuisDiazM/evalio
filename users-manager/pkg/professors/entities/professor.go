package entities

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Professor struct {
	ID        primitive.ObjectID `json:"id"  bson:"_id,omitempty"`
	Password  string             `json:"password,omitempty" bson:"password"`
	CreatedAt time.Time          `json:"created_at,omitempty" bson:"created_at"`
	UpdatedAt time.Time          `json:"updated_at,omitempty" bson:"updated_at"`
	Email     string             `json:"email,omitempty" bson:"email"`
	Name      string             `json:"name,omitempty" bson:"name"`
}
