package security

import (
	"os"
)

func LoadPrivateKey() ([]byte, error) {
	privateKey, err := os.ReadFile("private.pem")
	if err != nil {
		return nil, err
	}
	return privateKey, nil
}

func LoadPublicKey() ([]byte, error) {

	publicKey, err := os.ReadFile("public.pem")
	if err != nil {
		return nil, err
	}
	return publicKey, nil
}
