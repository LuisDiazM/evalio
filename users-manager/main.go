package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/LuisDiazM/evalio/users-manager/api/routers"
	"github.com/LuisDiazM/evalio/users-manager/infrastructure/database"
	"github.com/LuisDiazM/evalio/users-manager/infrastructure/logger"
	"github.com/LuisDiazM/evalio/users-manager/infrastructure/security"
	"github.com/LuisDiazM/evalio/users-manager/pkg/professors"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	// Inicializar el logger
	appLogger := logger.NewDefaultLogger(logger.INFO)
	ctx := context.TODO()
	// Cargar las claves RSA
	privateKey, err := security.LoadPrivateKey()
	if err != nil {
		appLogger.Fatal(ctx, "Failed to read private key", logger.NewField("error", err.Error()))
	}
	publicKey, err := security.LoadPublicKey()
	if err != nil {
		appLogger.Fatal(ctx, "Failed to read public key", logger.NewField("error", err.Error()))
	}

	if err != nil {
		appLogger.Fatal(ctx, "Failed to read public key", logger.NewField("error", err.Error()))
	}

	mongoClient, cancel, err := database.DatabaseConnection()
	if err != nil {
		panic(err)
	}
	// Inicializar el repositorio y el servicio
	professorRepo := professors.NewProfessorRepository(mongoClient.Collection("professors"))
	professorService := professors.NewProfessorService(professorRepo, appLogger, privateKey, publicKey)

	// Inicializar Fiber
	app := fiber.New()
	app.Use(cors.New())

	// Iniciar el servidor
	appLogger.Info(ctx, "Starting server on port 3000")

	api := app.Group("/users-manager")

	public := app.Group("/public")
	routers.PublicRoutes(public, professorService)
	routers.ProfessorRouter(api, professorService)
	defer cancel()
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	log.Fatal(app.Listen(fmt.Sprintf(`:%s`, port)))
}
