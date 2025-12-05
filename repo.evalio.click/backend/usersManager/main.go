package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/LuisDiazM/evalio/backend/usersManager/domain/professors/repositories"
	"github.com/LuisDiazM/evalio/backend/usersManager/domain/professors/usecases"
	"github.com/LuisDiazM/evalio/backend/usersManager/domain/shared"
	"github.com/LuisDiazM/evalio/backend/usersManager/infrastructure/database"
	"github.com/LuisDiazM/evalio/backend/usersManager/infrastructure/web/routes"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"go.mongodb.org/mongo-driver/mongo"
	"go.uber.org/fx"
)

type PrivateKey []byte
type PublicKey []byte

func NewFiberApp() *fiber.App {
	app := fiber.New()
	app.Use(cors.New())
	return app
}

func NewLogger() shared.Logger {
	return shared.NewDefaultLogger(shared.INFO)
}

// NewMongoCollection connects to MongoDB and returns the professors collection.
func NewMongoCollection(lc fx.Lifecycle) (*mongo.Collection, error) {
	db, cancel, err := database.DatabaseConnection()
	if err != nil {
		return nil, err
	}

	lc.Append(fx.Hook{
		OnStop: func(ctx context.Context) error {
			cancel()
			return nil
		},
	})

	return db.Collection("professors"), nil
}

// LoadKeys loads private and public PEM keys from disk (paths from env or defaults).
func LoadKeys() (PrivateKey, PublicKey, error) {
	privPath := os.Getenv("PRIVATE_PEM_PATH")
	pubPath := os.Getenv("PUBLIC_PEM_PATH")

	priv, err := os.ReadFile(privPath)
	if err != nil {
		return nil, nil, err
	}
	pub, err := os.ReadFile(pubPath)
	if err != nil {
		return nil, nil, err
	}
	return PrivateKey(priv), PublicKey(pub), nil
}

func NewProfessorUsecase(
	repo repositories.IProfessorRepository,
	logger shared.Logger,
	priv PrivateKey,
	pub PublicKey,
) usecases.IProfessorService {
	return usecases.NewProfessorService(repo, logger, []byte(priv), []byte(pub))
}

func RegisterPublicRoutes(app *fiber.App, service usecases.IProfessorService) {
	public := app.Group("/public")
	routes.PublicRoutes(public, service)
}

func StartServer(lc fx.Lifecycle, app *fiber.App) {
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	addr := fmt.Sprintf(":%s", port)

	lc.Append(fx.Hook{
		OnStart: func(ctx context.Context) error {
			go func() {
				if err := app.Listen(addr); err != nil {
					// Log the error; Fx lifecycle will handle shutdown.
					log.Printf("failed to listen: %v", err)
				}
			}()
			return nil
		},
		OnStop: func(ctx context.Context) error {
			return app.Shutdown()
		},
	})
}

func main() {
	app := fx.New(
		// infra
		fx.Provide(NewFiberApp),
		fx.Provide(NewLogger),
		fx.Provide(NewMongoCollection),
		// domain wiring
		fx.Provide(repositories.NewProfessorRepository),
		fx.Provide(LoadKeys),
		// service constructor uses (repo, logger, privateKey, publicKey)
		fx.Provide(NewProfessorUsecase),
		// route registration and lifecycle
		fx.Invoke(RegisterPublicRoutes),
		fx.Invoke(StartServer),
	)

	app.Run()
}
