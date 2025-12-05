package routes

import (
	"github.com/LuisDiazM/evalio/backend/usersManager/domain/professors/usecases"
	"github.com/LuisDiazM/evalio/backend/usersManager/infrastructure/web/handlers"
	"github.com/gofiber/fiber/v2"
)

func PublicRoutes(app fiber.Router, service usecases.IProfessorService) {
	app.Post("/signup", handlers.CreateProfessor(service))
	app.Post("/login", handlers.Login(service))
}
