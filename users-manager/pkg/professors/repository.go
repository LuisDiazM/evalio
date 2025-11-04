package professors

import (
	"context"
	"time"

	"github.com/LuisDiazM/evalio/users-manager/pkg/professors/entities"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

type IProfessorRepository interface {
	CreateProfessor(professor entities.Professor, ctx context.Context) (*entities.Professor, error)
	GetProfessor(email string, ctx context.Context) *entities.Professor
	UpdateProfessor(professor entities.Professor, ctx context.Context) error
	DeleteProfessor(email string, ctx context.Context) error
}

type repository struct {
	Collection *mongo.Collection
}

func NewProfessorRepository(collection *mongo.Collection) IProfessorRepository {
	return &repository{
		Collection: collection,
	}
}

// CreateProfessor implements IProfessorRepository.
func (r *repository) CreateProfessor(professor entities.Professor, ctx context.Context) (*entities.Professor, error) {
	professorCopy := professor
	professorCopy.ID = primitive.NewObjectID()
	professorCopy.CreatedAt = time.Now()
	professorCopy.UpdatedAt = time.Now()
	_, err := r.Collection.InsertOne(ctx, professor)
	if err != nil {
		return nil, err
	}
	return &professorCopy, nil
}

// DeleteProfessor implements IProfessorRepository.
func (r *repository) DeleteProfessor(id string, ctx context.Context) error {
	objectId, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		return err
	}
	_, err = r.Collection.DeleteOne(ctx, bson.M{"_id": objectId})
	if err != nil {
		return err
	}
	return nil
}

// GetProfessor implements IProfessorRepository.
func (r *repository) GetProfessor(email string, ctx context.Context) *entities.Professor {
	filter := bson.M{"email": email}
	var professor entities.Professor
	err := r.Collection.FindOne(ctx, filter).Decode(&professor)
	if err != nil {
		return nil
	}
	return &professor
}

// UpdateProfessor implements IProfessorRepository.
func (r *repository) UpdateProfessor(professor entities.Professor, ctx context.Context) error {
	professorCopy := professor
	professorCopy.UpdatedAt = time.Now()
	filter := bson.M{"email": professor.Email}
	update := bson.M{"$set": professorCopy}
	_, err := r.Collection.UpdateOne(ctx, filter, update)
	if err != nil {
		return err
	}
	return nil
}
