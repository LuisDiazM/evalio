package main

import (
	"crypto/rsa"
	"encoding/pem"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/golang-jwt/jwt/v5"
)

var (
	publicKey  *rsa.PublicKey
	errMissing = &fiber.Error{
		Code:    401,
		Message: "Missing JWT token",
	}
	errInvalid = &fiber.Error{
		Code:    401,
		Message: "Invalid JWT token",
	}
)

func loadPublicKey(path string) (*rsa.PublicKey, error) {
	keyData, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("error reading public key file: %v", err)
	}

	block, _ := pem.Decode(keyData)
	if block == nil {
		return nil, fmt.Errorf("failed to parse PEM block containing the public key")
	}

	publicKey, err := jwt.ParseRSAPublicKeyFromPEM(keyData)
	if err != nil {
		return nil, fmt.Errorf("error parsing public key: %v", err)
	}

	return publicKey, nil
}

func isPublicPath(path string) bool {
	return strings.HasPrefix(path, "/public")
}

func main() {
	var err error
	publicKey, err = loadPublicKey("public.pem")
	if err != nil {
		log.Fatalf("Error loading public key: %v", err)
	}

	app := fiber.New()
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins:     "http://localhost:5173,http://evalio.click,https://evalio.click,http://192.168.1.34:5173",
		AllowMethods:     "GET,POST,HEAD,PUT,DELETE,PATCH,OPTIONS",
		AllowHeaders:     "Origin, Content-Type, Accept, Authorization, X-Requested-With, X-User-Id, X-User-Email",
		ExposeHeaders:    "Content-Length, X-User-Id, X-User-Email",
		AllowCredentials: true,
		MaxAge:           100,
	}))

	// Middleware para debug de CORS
	app.Use(func(c *fiber.Ctx) error {
		// fmt.Printf("Request Origin: %s\n", c.Get("Origin"))
		// fmt.Printf("Request Method: %s\n", c.Method())
		// fmt.Printf("X-Forwarded-Method: %s\n", c.Get("X-Forwarded-Method"))
		// fmt.Printf("X-Forwarded-Uri: %s\n", c.Get("X-Forwarded-Uri"))
		// fmt.Printf("Request Headers: %v\n", c.GetReqHeaders())
		return c.Next()
	})

	// Middleware para validar rutas
	app.Use(func(c *fiber.Ctx) error {
		// Si es una petición OPTIONS, permitir el acceso
		if c.Method() == "OPTIONS" || c.Get("X-Forwarded-Method") == "OPTIONS" {
			return c.Next()
		}

		// Obtener el path original de la petición
		originalPath := c.Get("X-Forwarded-Uri")
		if originalPath == "" {
			originalPath = c.Path()
		}

		// Si es una ruta pública, permitir el acceso
		if isPublicPath(originalPath) {
			return c.Next()
		}

		// Para rutas protegidas, validar el token
		authHeader := c.Get("Authorization")
		if authHeader == "" {
			return c.Status(fiber.StatusUnauthorized).JSON(errMissing)
		}

		// Extraer el token del header Authorization
		tokenString := strings.TrimPrefix(authHeader, "Bearer ")
		if tokenString == authHeader {
			return c.Status(fiber.StatusUnauthorized).JSON(errMissing)
		}

		// Validar el token
		token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
			// Validar el método de firma
			if _, ok := token.Method.(*jwt.SigningMethodRSA); !ok {
				return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
			}
			return publicKey, nil
		})

		if err != nil {
			return c.Status(fiber.StatusUnauthorized).JSON(errInvalid)
		}

		if !token.Valid {
			return c.Status(fiber.StatusUnauthorized).JSON(errInvalid)
		}

		// Token válido, continuar
		return c.Next()
	})

	// Endpoint de autenticación
	app.Get("/auth", func(c *fiber.Ctx) error {
		// Si es una petición OPTIONS, responder con 200
		if c.Method() == "OPTIONS" || c.Get("X-Forwarded-Method") == "OPTIONS" {
			return c.SendStatus(fiber.StatusOK)
		}
		return c.SendStatus(fiber.StatusOK)
	})
	port := os.Getenv("PORT")
	if port == "" {
		port = "1337" // Default port if not set
	}
	log.Fatal(app.Listen(":" + port))
}
