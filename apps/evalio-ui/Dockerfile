# Multi-stage Dockerfile for evalio-ui with Bun + Nx.
# IMPORTANT: Build with the repository root as the Docker context, e.g.
#   docker build -f apps/evalio-ui/Dockerfile -t evalio-ui:latest .
FROM node:20-bullseye-slim AS builder

# Install tools for Bun installer and jq to edit nx.json
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl ca-certificates unzip jq \
  && rm -rf /var/lib/apt/lists/*

# Install Bun and add to PATH
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

WORKDIR /workspace

# Copy monorepo manifests needed for installing deps (from repo root)
COPY package.json bun.lock* nx.json tsconfig.base.json ./
COPY apps/evalio-ui/package.json apps/evalio-ui/project.json apps/evalio-ui/tsconfig*.json apps/evalio-ui/eslint.config.mjs apps/evalio-ui/rspack.config.js apps/evalio-ui/

# Ensure bun is available
RUN bun --version

# Install deps (cacheable)
RUN bun install

# Copy the rest of the repository (needed by Nx)
COPY . .
# Remove @nx-go/nx-go plugin and disable Nx Cloud to avoid auth prompts
RUN jq 'del(.nxCloudId) | .plugins |= map(select((.plugin? // .) != "@nx-go/nx-go"))' nx.json > nx.json.tmp && mv nx.json.tmp nx.json
RUN bun install --frozen-lockfile

# Force Nx CI mode without daemon/interactivity
ENV NX_NON_INTERACTIVE=true
ENV NX_DAEMON=false
ENV CI=true

# Build the app (production)
# Build the app (production)
RUN bunx nx build evalio-ui --configuration=development \
  && ls -R dist || true \
  && test -d dist/apps/evalio-ui


# Production image: serve static files with nginx on port 5000
FROM nginx:stable-alpine AS production

# Clean default nginx html
RUN rm -rf /usr/share/nginx/html/*

# Copy custom nginx config (listens on 5000)
COPY apps/evalio-ui/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /workspace/dist/apps/evalio-ui /usr/share/nginx/html
EXPOSE 5000
CMD ["nginx", "-g", "daemon off;"]
