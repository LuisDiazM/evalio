package database

import (
	"context"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	DATABASE_NAME = "users-manager"
)

func DatabaseConnection() (*mongo.Database, context.CancelFunc, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
	mongoUrl := os.Getenv("MONGO_URL")
	if mongoUrl == "" {
		panic("MONGO_URL is not set")
	}
	client, err := mongo.Connect(ctx, options.Client().ApplyURI(
		mongoUrl).SetServerSelectionTimeout(5*time.
		Second))
	if err != nil {
		cancel()
		return nil, nil, err
	}
	db := client.Database(DATABASE_NAME)
	return db, cancel, nil
}
