package routes

import (
	"github.com/LuisDiazM/evalio/evalio-manager/api/handlers"
	"github.com/LuisDiazM/evalio/evalio-manager/pkg/students"
	"github.com/gofiber/fiber/v2"
)

func StudentRouter(app fiber.Router, service students.IStudentsService) {
	app.Post("/students", handlers.AddStudents(service))
}
