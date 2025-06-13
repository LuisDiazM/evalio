package professors

import (
	"context"
	"errors"
	"time"

	"github.com/LuisDiazM/evalio/users-manager/infrastructure/logger"
	"github.com/LuisDiazM/evalio/users-manager/pkg/professors/entities"
	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

type ProfessorClaims struct {
	Email       string `json:"email"`
	Name        string `json:"name"`
	ProfessorId string `json:"professor_id"`
	jwt.RegisteredClaims
}

type IProfessorService interface {
	CreateProfessor(professor entities.Professor, ctx context.Context) (string, error)
	GetProfessor(email string, ctx context.Context) *entities.Professor
	UpdateProfessor(professor entities.Professor, ctx context.Context) error
	DeleteProfessor(email string, ctx context.Context) error
	Authenticate(email string, password string, ctx context.Context) (string, string, error)
}

type ProfessorService struct {
	repo       IProfessorRepository
	logger     logger.Logger
	privateKey []byte
	publicKey  []byte
}

func NewProfessorService(repo IProfessorRepository, logger logger.Logger, privateKey, publicKey []byte) IProfessorService {
	return &ProfessorService{
		repo:       repo,
		logger:     logger,
		privateKey: privateKey,
		publicKey:  publicKey,
	}
}

func (s *ProfessorService) Authenticate(email string, password string, ctx context.Context) (string, string, error) {
	professor := s.GetProfessor(email, ctx)
	if professor == nil {
		return "", "", errors.New("professor not found")
	}

	err := bcrypt.CompareHashAndPassword([]byte(professor.Password), []byte(password))
	if err != nil {
		return "", "", errors.New("invalid password")
	}
	expiresAt := time.Now().Add(8 * time.Hour)
	// Crear claims del token
	claims := ProfessorClaims{
		Email:       professor.Email,
		Name:        professor.Name,
		ProfessorId: professor.ID.Hex(),
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expiresAt),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			NotBefore: jwt.NewNumericDate(time.Now()),
		},
	}

	// Crear el token
	token := jwt.NewWithClaims(jwt.SigningMethodRS256, claims)

	// Firmar el token con la clave privada
	key, err := jwt.ParseRSAPrivateKeyFromPEM(s.privateKey)
	if err != nil {
		s.logger.Error(ctx, "failed to parse private key", logger.NewField("error", err.Error()))
		return "", "", errors.New("internal server error")
	}

	tokenString, err := token.SignedString(key)
	if err != nil {
		s.logger.Error(ctx, "failed to sign token", logger.NewField("error", err.Error()))
		return "", "", errors.New("internal server error")
	}

	return tokenString, expiresAt.Local().String(), nil
}

func (s *ProfessorService) CreateProfessor(professor entities.Professor, ctx context.Context) (string, error) {
	// Hashear la contraseña antes de guardar
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(professor.Password), bcrypt.DefaultCost)
	if err != nil {
		errorMsg := "Failed to hash password: " + err.Error()
		s.logger.Error(ctx, errorMsg,
			logger.NewField("email", professor.Email))
		return "", errors.New(errorMsg)
	}

	// Reemplazar la contraseña plana con el hash
	professor.Password = string(hashedPassword)
	professor.CreatedAt = time.Now()
	professor.UpdatedAt = time.Now()

	response, err := s.repo.CreateProfessor(professor, ctx)
	if err != nil {
		errorMsg := "failed to create professor exists"
		s.logger.Error(ctx, errorMsg,
			logger.NewField("email", professor.Email),
			logger.NewField("error", err.Error()))
		return "", errors.New(errorMsg)
	}

	s.logger.Info(ctx, "Professor created successfully",
		logger.NewField("id", response.ID.String()),
		logger.NewField("email", professor.Email))
	return response.ID.String(), nil
}

func (s *ProfessorService) GetProfessor(email string, ctx context.Context) *entities.Professor {

	professor := s.repo.GetProfessor(email, ctx)
	if professor == nil {
		s.logger.Warn(ctx, "Professor not found", logger.NewField("email", email))
		return nil
	}
	return professor
}

func (s *ProfessorService) UpdateProfessor(professor entities.Professor, ctx context.Context) error {
	professorData := s.GetProfessor(professor.Email, ctx)
	if professorData == nil {
		return errors.New("professor not found")
	}
	professor.ID = professorData.ID
	professor.CreatedAt = professorData.CreatedAt
	professor.UpdatedAt = time.Now()
	if professor.Password != "" {

		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(professor.Password), bcrypt.DefaultCost)
		if err != nil {
			errorMsg := "Failed to hash password: " + err.Error()
			s.logger.Error(ctx, errorMsg,
				logger.NewField("email", professor.Email))
			return errors.New(errorMsg)
		}

		professor.Password = string(hashedPassword)
	} else {
		professor.Password = professorData.Password
	}
	err := s.repo.UpdateProfessor(professor, ctx)
	if err != nil {
		s.logger.Error(ctx, "Failed to update professor",
			logger.NewField("id", professor.ID.String()),
			logger.NewField("email", professor.Email),
			logger.NewField("error", err.Error()))
		return err
	}
	return nil
}

func (s *ProfessorService) DeleteProfessor(email string, ctx context.Context) error {
	err := s.repo.DeleteProfessor(email, ctx)
	if err != nil {
		s.logger.Error(ctx, "Failed to delete professor",
			logger.NewField("email", email),
			logger.NewField("error", err.Error()))
		return err
	}

	s.logger.Info(ctx, "Professor deleted successfully", logger.NewField("email", email))
	return nil
}

// VerifyPassword verifica si la contraseña proporcionada coincide con el hash almacenado
func (s *ProfessorService) VerifyPassword(hashedPassword, plainPassword string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(plainPassword))
	return err == nil
}
