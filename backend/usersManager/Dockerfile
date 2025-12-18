# syntax=docker/dockerfile:1.4
## Multi-stage Dockerfile for usersManager (Go 1.23)
## Builder: compiles the binary and produces a static binary
## Runner: minimal distroless static image running as non-root

FROM golang:1.23.11-bullseye AS builder
WORKDIR /src

# Build-time environment: produce a static, optimized binary
ENV CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Copy go.mod / go.sum first to cache `go mod download`
COPY go.mod go.sum ./

# Download module dependencies
RUN go mod download

# Copy the rest of the sources
COPY . .

# Build the binary with optimizations and smaller symbol table
# -trimpath removes file system paths from the binary
# -ldflags "-s -w" strips debug information
RUN go build -trimpath -o /usr/local/bin/usersmanager -ldflags "-s -w" ./main.go

### Final image: minimal runtime
FROM gcr.io/distroless/static:nonroot

LABEL org.opencontainers.image.source="github.com/LuisDiazM/evalio" \
      org.opencontainers.image.title="usersManager" \
      org.opencontainers.image.licenses="MIT"

# Copy the statically linked binary from the builder stage
COPY --from=builder /usr/local/bin/usersmanager /usr/local/bin/usersmanager

# Use an unprivileged user provided by the distroless image
USER nonroot:nonroot

# The service listens on 3000 by default (see main.go)
EXPOSE 3000

ENTRYPOINT ["/usr/local/bin/usersmanager"]

## Notes:
# docker build -f backend/usersManager/Dockerfile -t usersmanager:latest backend/usersManager
