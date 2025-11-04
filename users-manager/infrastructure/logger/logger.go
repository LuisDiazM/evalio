package logger

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"
)

// Level representa el nivel de logging
type Level int

const (
	DEBUG Level = iota
	INFO
	WARN
	ERROR
	FATAL
)

// String retorna el string representativo del nivel
func (l Level) String() string {
	switch l {
	case DEBUG:
		return "DEBUG"
	case INFO:
		return "INFO"
	case WARN:
		return "WARN"
	case ERROR:
		return "ERROR"
	case FATAL:
		return "FATAL"
	default:
		return "UNKNOWN"
	}
}

// Logger es la interfaz que define los métodos de logging
type Logger interface {
	Debug(ctx context.Context, message string, fields ...Field)
	Info(ctx context.Context, message string, fields ...Field)
	Warn(ctx context.Context, message string, fields ...Field)
	Error(ctx context.Context, message string, fields ...Field)
	Fatal(ctx context.Context, message string, fields ...Field)
}

// Field representa un campo adicional en el log
type Field struct {
	Key   string
	Value interface{}
}

// NewField crea un nuevo Field
func NewField(key string, value interface{}) Field {
	return Field{
		Key:   key,
		Value: value,
	}
}

// DefaultLogger es una implementación básica de Logger
type DefaultLogger struct {
	level Level
}

// NewDefaultLogger crea una nueva instancia de DefaultLogger
func NewDefaultLogger(level Level) *DefaultLogger {
	return &DefaultLogger{
		level: level,
	}
}

// log es el método interno que maneja el logging
func (l *DefaultLogger) log(ctx context.Context, level Level, message string, fields ...Field) {
	if level < l.level {
		return
	}

	timestamp := time.Now().Format(time.RFC3339)
	logMessage := fmt.Sprintf("[%s] %s: %s", timestamp, level.String(), message)

	// Agregar campos adicionales
	for _, field := range fields {
		logMessage += fmt.Sprintf(" %s=%v", field.Key, field.Value)
	}

	// Por ahora usamos el logger estándar de Go
	log.Println(logMessage)
}

func (l *DefaultLogger) Debug(ctx context.Context, message string, fields ...Field) {
	l.log(ctx, DEBUG, message, fields...)
}

func (l *DefaultLogger) Info(ctx context.Context, message string, fields ...Field) {
	l.log(ctx, INFO, message, fields...)
}

func (l *DefaultLogger) Warn(ctx context.Context, message string, fields ...Field) {
	l.log(ctx, WARN, message, fields...)
}

func (l *DefaultLogger) Error(ctx context.Context, message string, fields ...Field) {
	l.log(ctx, ERROR, message, fields...)
}

func (l *DefaultLogger) Fatal(ctx context.Context, message string, fields ...Field) {
	l.log(ctx, FATAL, message, fields...)
	os.Exit(1)
}
