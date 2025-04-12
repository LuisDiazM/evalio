package students

import (
	"encoding/csv"
	"fmt"
)

type IStudentsService interface {
	CreateStudents(csvReader *csv.Reader, groupId string) error
}

type StudentsService struct {
}

func NewStudentsService() IStudentsService {
	return &StudentsService{}
}

func (s *StudentsService) CreateStudents(csvReader *csv.Reader, groupId string) error {
	headers, _ := csvReader.Read()
	fmt.Println(headers)
	return nil
}
