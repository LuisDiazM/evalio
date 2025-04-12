package handlers

import (
	"encoding/csv"
	"io"
	"net/http"

	"github.com/LuisDiazM/evalio/evalio-manager/pkg/students"
	"github.com/gofiber/fiber/v2"
)

const (
	MAX_FILE_SIZE = 1 * 1024 * 1024 //15 Mb
)

func AddStudents(studentService students.IStudentsService) fiber.Handler {
	return func(c *fiber.Ctx) error {
		file, err := c.FormFile("file")
		groupId := c.FormValue("group_id")
		if file.Size > MAX_FILE_SIZE {
			return fiber.NewError(fiber.StatusRequestEntityTooLarge, "error with file")
		}
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, err.Error())
		}
		src, err := file.Open()
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, err.Error())
		}
		defer src.Close()

		buffer := make([]byte, 512)
		if _, err := src.Read(buffer); err != nil && err != io.EOF {
			return fiber.NewError(fiber.StatusInternalServerError, err.Error())
		}

		contentType := http.DetectContentType(buffer)
		if contentType != "text/plain; charset=utf-8" {
			return fiber.NewError(fiber.StatusBadRequest, "file not allowed")
		}

		// Procesar
		reader := csv.NewReader(src)
		_, err = reader.Read()
		if err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, err.Error())
		}

		if err := studentService.CreateStudents(reader, groupId); err != nil {
			return fiber.NewError(fiber.StatusInternalServerError, err.Error())
		}
		return c.JSON(nil)
	}
}
