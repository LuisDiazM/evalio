package students

import (
	"encoding/csv"
	"fmt"
	"io"
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
	// var students []entities.StudentCSV
	for {
		record, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}

		if err != nil {
			panic(err)
		}
		fmt.Println(record)

	}
	return nil
}
