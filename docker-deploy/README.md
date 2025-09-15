# Immigration Pathfinder Agent

A Langflow-based application that helps users find immigration paths, with PostgreSQL database backend and Docker deployment.

## Features

- AI-powered immigration pathfinding
- PostgreSQL database integration
- Dockerized deployment
- Vector database (Chroma) for document processing
- Memory component for conversation history
- Groq language model integration

## Quick Start

To start the application:

1. First navigate to the deploy directory:

    ```bash
    cd docker-deploy
    ```

2. Following [Configuration](#configuration) to set `.env` file.

3. Start the services (this will use both docker-compose.yml and docker-compose.override.yml):

    ```bash
    docker-compose up -d
    ```

The application will be available at: [http://localhost:7860](http://localhost:7860)

Note: The docker-compose.override.yml file contains additional service configurations that will be merged with the base docker-compose.yml file.

## Configuration

### Initial Setup

1. Copy the example environment file:

    ```bash
    cp .env.example .env
    ```

2. Edit the `.env` and add your Groq API key (if using the Groq model) or any other keys. If you want to use other models, edit them in the Langflow UI first, then export the workflow to the `flows` folder and select `Save with my API keys`.

3. Add your documents in `rag_docs`
4. Run

    ```bash
    docker network create traefik-public
    ```

    or set `TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL=true` in `.env` for local dev

### Environment Variables

Key environment variables:

- `LANGFLOW_DATABASE_URL`: PostgreSQL connection string (default: `postgresql://langflow:langflow@postgres:5432/langflow`)
- `LANGFLOW_CONFIG_DIR`: Path for configuration files (default: `app/langflow`)
- Model-specific variables (check .env.example for complete list)

### Database

PostgreSQL service is configured with:

- User: `langflow`
- Password: `langflow`
- Database: `langflow`
- Port: `5432`

## Advanced Configuration

Additional environment variables from .env.example:

### Server Settings

- `LANGFLOW_HOST`: Server host (default: empty)
- `LANGFLOW_PORT`: Server port (default: `7860`)
- `LANGFLOW_WORKERS`: Worker processes count

### Logging

- `LANGFLOW_LOG_LEVEL`: Logging level (e.g. `critical`, `error`, `warning`, `info`, `debug`)
- `LANGFLOW_LOG_FILE`: Path to log file
- `LANGFLOW_LOG_ROTATION`: Log rotation policy

### Authentication

- `LANGFLOW_AUTO_LOGIN`: Enable/disable auto login
- `LANGFLOW_SUPERUSER`: Admin username
- `LANGFLOW_SUPERUSER_PASSWORD`: Admin password

### Cache

- `LANGFLOW_CACHE_TYPE`: Cache type (`async`, `memory`, `redis`)
- Redis-specific settings:
  - `LANGFLOW_REDIS_HOST`: Redis host (default: `result_backend`)
  - `LANGFLOW_REDIS_PORT`: Redis port (default: `6379`)
  - `LANGFLOW_REDIS_DB`: Redis database number (default: `0`)
  - `LANGFLOW_REDIS_EXPIRE`: Cache expiration in seconds (default: `3600`)
  - `LANGFLOW_REDIS_PASSWORD`: Redis password (default: empty)

### Message Queue (RabbitMQ)

- `BROKER_URL`: AMQP connection URL (default: `amqp://langflow:langflow@broker:5672`)
- `RESULT_BACKEND`: Result backend URL (default: `redis://result_backend:6379/0`)
- `RABBITMQ_DEFAULT_USER`: RabbitMQ username (default: `langflow`)
- `RABBITMQ_DEFAULT_PASS`: RabbitMQ password (default: `langflow`)

### Database Admin (PGAdmin)

- `PGADMIN_DEFAULT_EMAIL`: PGAdmin login email (default: `admin@admin.com`)
- `PGADMIN_DEFAULT_PASSWORD`: PGAdmin login password (default: `admin`)

### Traefik Configuration

- `TRAEFIK_PUBLIC_NETWORK`: Traefik public network name (default: `traefik-public`)
- `TRAEFIK_TAG`: Traefik service tag (default: `langflow-traefik`)
- `TRAEFIK_PUBLIC_TAG`: Traefik public tag (default: `traefik-public`)

### Flower Configuration

- `FLOWER_UNAUTHENTICATED_API`: Enable unauthenticated API access (default: `True`)
- `C_FORCE_ROOT`: Force root user (default: `"true"`)

## Data Persistence

Data is persisted in Docker volumes:

- `langflow-postgres`: Stores PostgreSQL database files
- `langflow-data`: Stores application configuration and data

## Ports

- Application UI: `7860`
- PostgreSQL: `5432`

## Application Components

The current workflow configuration includes:

- **Groq Language Model**: For AI responses (requires API key)
- **LM Studio Embeddings**: Local embeddings model
- **Chroma Vector Database**: For document processing
- **Memory Component**: Conversation history

To modify the workflow:

1. Access the Langflow UI at [http://localhost:7860](http://localhost:7860)
2. Make your changes to the workflow
3. Export the updated flow JSON
4. Replace the flows/flatopia-deploy.json file with your updated version
5. Restart the services

## Version Information

- Last tested with Langflow version: 1.5.1
