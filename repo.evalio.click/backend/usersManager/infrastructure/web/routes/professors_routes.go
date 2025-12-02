package routes

import "github.com/gofiber/fiber/v2"

func PublicRoutes(app fiber.Router) {
	app.Post("/signup", nil)
	app.Post("/login", nil)
}
