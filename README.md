# IIS_project - DJKhaled's Animal Shelter (30b/30)
Adam Valík (xvalik05) - vedoucí <br>
Marek EffenBerger (xeffen00) <br>
Samuel Hejníček (xhejni00) <br>

This project uses Docker Compose, which is included with Docker Desktop (download from [docker.com](https://www.docker.com/products/docker-desktop/))

## Project Structure

- backend: Contains the FastAPI backend code.
- web-app: Contains the Vue.js frontend code.
- doc: Placeholder directory.
- docker-compose.yml: Docker Compose configuration to manage all services.
- postgres_data: Docker volume for PostgreSQL persistent storage.

## Using Docker Compose
> **Note**: If the command `docker-compose` does not work, try using `docker compose` (without the hyphen) instead.

| Command                                | Description                                           |
|----------------------------------------|-------------------------------------------------------|
| `docker-compose build`                 | Builds all services in the `docker-compose.yml`.      |
| `docker-compose build <service_name>`  | Builds a single service (e.g., `web-app`, `backend`). |
| `docker-compose up --build`            | Rebuilds and restarts containers.                     |
| `docker-compose up`                    | Starts all services in the foreground.                |
| `docker-compose up -d`                 | Starts all services in detached mode (background).    |
| `docker-compose down`                  | Stops and removes all containers.                     |
| `docker-compose down -v`               | Stops containers and removes volumes (data cleanup).  |
| `docker-compose logs <service_name>`   | Shows logs for a specific service.                    |
| `docker-compose exec <service_name> sh`| Opens a shell in a specific running container.        |
| `docker ps`                            | Lists all currently running Docker containers.        |

### Commands inside the docker
Run example_data.py to fill the database with example data
```bash
docker exec -it backend python3 /app/example_data.py
```

Open postgresql database shell
```bash
docker exec -it postgres psql -U user -d animal_shelter_db
```

## Running the Project

Services will be available at:
- [http://localhost:8080](http://localhost:8080) - Web App frontend
- [http://localhost:8000](http://localhost:8000) - FastAPI backend
- [http://localhost:5432](http://localhost:5432) - PostgreSQL database

API Documentation:
- [http://localhost:8000/docs](http://localhost:8000/docs) - FastAPI Swagger UI
- [http://localhost:8000/redoc](http://localhost:8000/redoc) - FastAPI Redoc UI

# If problems with permission in node-modules
- Run containers as docker compuse -up
- Navigate to web-app container
```bash
docker exec -it web-app bash
```
- apply permissions
```bash
chmod -R 777 ./node_modules
```
