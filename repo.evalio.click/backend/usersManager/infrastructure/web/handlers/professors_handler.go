package handlers

import (
	"net/http"

	"github.com/LuisDiazM/evalio/backend/usersManager/domain/professors/entities"
	"github.com/LuisDiazM/evalio/backend/usersManager/domain/professors/usecases"
	"github.com/LuisDiazM/evalio/backend/usersManager/infrastructure/web/presenters"
	"github.com/gofiber/fiber/v2"
)

func Login(service usecases.IProfessorService) fiber.Handler {
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

func CreateProfessor(service usecases.IProfessorService) fiber.Handler {
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
