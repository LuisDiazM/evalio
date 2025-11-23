package handlers

import (
	"net/http"

	"github.com/LuisDiazM/evalio/users-manager/api/presenters"
	"github.com/LuisDiazM/evalio/users-manager/pkg/professors"
	"github.com/LuisDiazM/evalio/users-manager/pkg/professors/entities"
	"github.com/gofiber/fiber/v2"
)

func CreateProfessor(service professors.IProfessorService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		var requestBody presenters.ProfessorRequest

		err := c.BodyParser(&requestBody)
		if err != nil {
			c.Status(http.StatusBadRequest)
			return c.JSON(presenters.ProfessorErrorResponse{Error: err.Error()})
		}
		professor := entities.Professor{
			Password: requestBody.Password,
			Email:    requestBody.Email,
			Name:     requestBody.Name,
		}
		result, err := service.CreateProfessor(professor, c.Context())
		if err != nil {
			c.Status(http.StatusInternalServerError)
			return c.JSON(presenters.ProfessorErrorResponse{Error: err.Error()})
		}
		c.Status(http.StatusCreated)
		return c.JSON(presenters.ProfessorResponse{ID: result})
	}
}

func Login(service professors.IProfessorService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		var requestBody presenters.LoginRequest
		err := c.BodyParser(&requestBody)
		if err != nil {
			c.Status(http.StatusBadRequest)
			return c.JSON(presenters.ProfessorErrorResponse{Error: err.Error()})
		}
		token, expiration, err := service.Authenticate(requestBody.Email, requestBody.Password, c.Context())
		if err != nil {
			c.Status(http.StatusUnauthorized)
			return c.JSON(presenters.ProfessorErrorResponse{Error: "Invalid email or password"})
		}
		return c.JSON(presenters.LoginResponse{
			Token:     token,
			ExpiresAt: expiration,
		})
	}
}

func UpdateProfessor(service professors.IProfessorService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		var requestBody presenters.ProfessorRequest
		err := c.BodyParser(&requestBody)
		if err != nil {
			c.Status(http.StatusBadRequest)
			return c.JSON(presenters.ProfessorErrorResponse{Error: err.Error()})
		}
		professor := entities.Professor{
			Email:    requestBody.Email,
			Name:     requestBody.Name,
			Password: requestBody.Password,
		}
		err = service.UpdateProfessor(professor, c.Context())
		if err != nil {
			c.Status(http.StatusInternalServerError)
			return c.JSON(presenters.ProfessorErrorResponse{Error: err.Error()})
		}
		return c.JSON("ok")
	}
}

func GetProfesorByEmail(service professors.IProfessorService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		email := c.Query("email")
		if email == "" {
			c.Status(http.StatusBadRequest)
			return c.JSON(presenters.ProfessorErrorResponse{Error: "Email query parameter is required"})
		}
		professor := service.GetProfessor(email, c.Context())
		if professor == nil {
			c.Status(http.StatusNotFound)
			return c.JSON(presenters.ProfessorErrorResponse{Error: "Professor not found"})
		}
		response := presenters.ProfessorInfo{
			ID:        professor.ID.Hex(),
			CreatedAt: professor.CreatedAt,
			UpdatedAt: professor.UpdatedAt,
			Email:     professor.Email,
			Name:      professor.Name,
		}
		return c.JSON(response)
	}
}
