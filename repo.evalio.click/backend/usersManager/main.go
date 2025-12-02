package main

import (
	"fmt"
	"log"
	"os"

	"github.com/LuisDiazM/evalio/backend/usersManager/infrastructure/web/routes"
	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
	app := fiber.New()
	app.Use(cors.New())
	public := app.Group("/public")
	routes.PublicRoutes(public)
	port := os.Getenv("PORT")
	if port == "" {
		port = "3000"
	}
	log.Fatal(app.Listen(fmt.Sprintf(`:%s`, port)))
}
