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

func tryLoadEnv() error {
	f, err := os.Open(".env")
	if err != nil {
		if os.IsNotExist(err) {
			return nil
		}
		return err
	}
	defer f.Close()
	return nil
}

func isPublicPath(path string) bool {
	return strings.HasPrefix(path, "/public")
}

func main() {
	// Attempt to load .env optionally; not fatal if .env is missing
	if err := tryLoadEnv(); err != nil {
		log.Printf("warning: error loading .env: %v", err)
	}

	// Determine public key path from env var or fallback locations
	pubPath := os.Getenv("PUBLIC_PEM_PATH")
	if pubPath == "" {
		// try common locations relative to repo
		pubPath = "configs/certs/public.pem"
		// final fallback to local file
		if _, err := os.Stat(pubPath); os.IsNotExist(err) {
			if _, err2 := os.Stat("public.pem"); err2 == nil {
				pubPath = "public.pem"
			}
		}
	}

	var err error
	publicKey, err = loadPublicKey(pubPath)
	if err != nil {
		log.Printf("warning: could not load public key from '%s': %v", pubPath, err)
		publicKey = nil
	}

	app := fiber.New()
	app.Use(logger.New())
	app.Use(cors.New(cors.Config{
		AllowOrigins:     "http://localhost:5000,https://evalio.click",
		AllowMethods:     "GET,POST,HEAD,PUT,DELETE,PATCH,OPTIONS",
		AllowHeaders:     "Origin, Content-Type, Accept, Authorization, X-Requested-With, X-User-Id, X-User-Email",
		ExposeHeaders:    "Content-Length, X-User-Id, X-User-Email",
		AllowCredentials: true,
		MaxAge:           100,
	}))

	// Middleware para debug de CORS
	app.Use(func(c *fiber.Ctx) error {
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
			if publicKey == nil {
				return nil, fmt.Errorf("no public key available for verification")
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
