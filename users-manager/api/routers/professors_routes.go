package routers

import (
	"github.com/LuisDiazM/evalio/users-manager/api/handlers"
	"github.com/LuisDiazM/evalio/users-manager/pkg/professors"
	"github.com/gofiber/fiber/v2"
)

func ProfessorRouter(app fiber.Router, service professors.IProfessorService) {
	app.Put("/professor", handlers.UpdateProfessor(service))
}

func PublicRoutes(app fiber.Router, service professors.IProfessorService) {
	app.Post("/signup", handlers.CreateProfessor(service))
	app.Post("/login", handlers.Login(service))
}
