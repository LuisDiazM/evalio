#!/usr/bin/env fish

# Environment Switcher Script
# Usage: ./run-env.fish [dev|qa|prod]

set env_name $argv[1]

# Default to development if no argument
if test -z "$env_name"
    set env_name "dev"
end

switch $env_name
    case dev development
        echo "🔧 Starting DEVELOPMENT environment..."
        set -x APP_ENV development
        set -x NODE_ENV development

    case qa staging
        echo "🧪 Starting QA environment..."
        set -x APP_ENV qa
        set -x NODE_ENV development

    case prod production
        echo "🚀 Building for PRODUCTION environment..."
        set -x APP_ENV production
        set -x NODE_ENV production

    case '*'
        echo "❌ Unknown environment: $env_name"
        echo ""
        echo "Usage: ./run-env.fish [dev|qa|prod]"
        echo ""
        echo "Examples:"
        echo "  ./run-env.fish dev   # Start development server"
        echo "  ./run-env.fish qa    # Start with QA config"
        echo "  ./run-env.fish prod  # Build for production"
        exit 1
end

echo "Environment: $APP_ENV"
echo "Node ENV: $NODE_ENV"
echo ""

# Run appropriate command
if test "$NODE_ENV" = "production"
    echo "Building application..."
    bun nx run @evalio.click/evalio-ui:build
else
    echo "Starting dev server..."
    bun nx run @evalio.click/evalio-ui:serve
end
