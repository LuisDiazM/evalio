package main

import (
	"log"

	"github.com/LuisDiazM/evalio/evalio-manager/api/routes"
	"github.com/LuisDiazM/evalio/evalio-manager/pkg/students"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	// Fiber instance
	app := fiber.New()
	app.Use(cors.New())

	//Services
	studentService := students.NewStudentsService()

	// Routes
	api := app.Group("/api")
	routes.StudentRouter(api, studentService)
	// Start server
	log.Fatal(app.Listen(":3000"))
}
